"""
Comprehensive LLM Router Evaluation Script
Tests all routers across 5 categories with detailed metrics

Author: Ata Jodeiri Seyedian
Project: LLM-based customer service routing system 
"""

import json
import time
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routers.llm_router import LLMRouter


class RouterEvaluator:
    """Comprehensive evaluation framework for LLM routers"""
    
    def __init__(self):
        """Initialize evaluator with all test data"""
        self.test_categories = {
            'basic': 'tests/test_queries.json',
            'edge_cases': 'tests/edge_cases.json',
            'clinical_safety': 'tests/clinical_safety.json',
            'hallucination': 'tests/hallucination_tests.json',
            'uncertainty': 'tests/uncertainty_tests.json'
        }
        
        self.test_data = {}
        self.results = {}
        
        print("=" * 80)
        print("Evaluation Started...")
        print("=" * 80)
        print(f"Evaluation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80 + "\n")
        
        self._load_test_data()
    
    
    def _load_test_data(self):
        """Load all test data files"""
        print("Loading test data...\n")
        
        for category, filepath in self.test_categories.items():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Extract test cases based on category
                    if category == 'basic':
                        self.test_data[category] = data['test_queries']
                    elif category == 'edge_cases':
                        self.test_data[category] = data['edge_cases']
                    elif category == 'clinical_safety':
                        self.test_data[category] = data['clinical_safety']
                    elif category == 'hallucination':
                        self.test_data[category] = data['hallucination_tests']
                    elif category == 'uncertainty':
                        self.test_data[category] = data['uncertainty_tests']
                    
                    print(f"  Loaded {len(self.test_data[category])} {category} test cases")
                    
            except FileNotFoundError:
                print(f"  Warning: {filepath} not found, skipping {category}")
                self.test_data[category] = []
            except Exception as e:
                print(f"  Error loading {filepath}: {e}")
                self.test_data[category] = []
        
        total = sum(len(tests) for tests in self.test_data.values())
        print(f"\nTotal test cases loaded: {total}\n")
    
    
    def evaluate_router(self, mode):
        """
        Evaluate a single router mode across all test categories
        
        Args:
            mode: Router mode ('simple', 'gemini', 'gpt')
        
        Returns:
            Dictionary with detailed results
        """
        print("\n" + "=" * 80)
        print(f" EVALUATING: {mode.upper()} ROUTER")
        print("=" * 80 + "\n")
        
        # Initialize router
        try:
            router = LLMRouter(mode=mode)
        except Exception as e:
            print(f" Failed to initialize {mode} router: {e}")
            return None
        
        # Results structure
        results = {
            'mode': mode,
            'categories': {},
            'overall': {
                'total_queries': 0,
                'correct': 0,
                'incorrect': 0,
                'accuracy': 0.0,
                'avg_response_time': 0.0,
                'total_time': 0.0
            }
        }
        
        total_correct = 0
        total_queries = 0
        total_time = 0.0
        
        # Evaluate each category
        for category, test_cases in self.test_data.items():
            if not test_cases:
                continue
            
            print(f"\n Testing {category.upper().replace('_', ' ')} ({len(test_cases)} queries)...")
            
            category_results = {
                'total': len(test_cases),
                'correct': 0,
                'incorrect': 0,
                'accuracy': 0.0,
                'errors': [],
                'response_times': []
            }
            
            for test in test_cases:
                query = test['query']
                expected = test['expected_agent']
                
                # Time the routing
                start_time = time.time()
                try:
                    actual_agent, answer = router.route(query)
                    response_time = time.time() - start_time

                    # Add delay for Gemini to respect rate limits (10 req/min = 6s minimum)
                    if mode == 'gemini':
                        time.sleep(7)  # To avoid rate limits


                except Exception as e:
                    print(f"   Error on query '{query[:50]}...': {e}")
                    category_results['incorrect'] += 1
                    continue
                
                category_results['response_times'].append(response_time)
                total_time += response_time
                
                # Check if routing is correct
                if actual_agent == expected:
                    category_results['correct'] += 1
                    total_correct += 1
                else:
                    category_results['incorrect'] += 1
                    category_results['errors'].append({
                        'query': query,
                        'expected': expected,
                        'actual': actual_agent,
                        'test_id': test.get('id', 'N/A')
                    })
            
            # Calculate category accuracy
            if category_results['total'] > 0:
                category_results['accuracy'] = (category_results['correct'] / category_results['total']) * 100
            
            # Calculate average response time for category
            if category_results['response_times']:
                category_results['avg_response_time'] = sum(category_results['response_times']) / len(category_results['response_times'])
            else:
                category_results['avg_response_time'] = 0.0
            
            results['categories'][category] = category_results
            total_queries += category_results['total']
            
            # Print category summary
            print(f"   Correct: {category_results['correct']}/{category_results['total']}")
            print(f"   Accuracy: {category_results['accuracy']:.1f}%")
            print(f"   Avg Response Time: {category_results['avg_response_time']:.3f}s")
        
        # Calculate overall results
        if total_queries > 0:
            results['overall']['total_queries'] = total_queries
            results['overall']['correct'] = total_correct
            results['overall']['incorrect'] = total_queries - total_correct
            results['overall']['accuracy'] = (total_correct / total_queries) * 100
            results['overall']['total_time'] = total_time
            results['overall']['avg_response_time'] = total_time / total_queries
        
        # Print overall summary
        print(f"\n{'=' * 80}")
        print(f" {mode.upper()} ROUTER - OVERALL RESULTS")
        print(f"{'=' * 80}")
        print(f"Total Queries:        {results['overall']['total_queries']}")
        print(f"Correct:              {results['overall']['correct']}")
        print(f"Incorrect:            {results['overall']['incorrect']}")
        print(f"Overall Accuracy:     {results['overall']['accuracy']:.1f}%")
        print(f"Avg Response Time:    {results['overall']['avg_response_time']:.3f}s")
        print(f"Total Evaluation Time: {results['overall']['total_time']:.2f}s")
        print(f"{'=' * 80}\n")
        
        return results
    
    
    def compare_routers(self, modes=['simple', 'gemini', 'gpt']):
        """
        Compare multiple routers and generate comparison report
        
        Args:
            modes: List of router modes to compare
        """
        print("\n" + "=" * 80)
        print(" ROUTER COMPARISON")
        print("=" * 80 + "\n")
        
        all_results = {}
        
        # Evaluate each router
        for mode in modes:
            results = self.evaluate_router(mode)
            if results:
                all_results[mode] = results
        
        # Generate comparison table
        self._generate_comparison_table(all_results)
        
        # Generate detailed report
        self._generate_detailed_report(all_results)
        
        return all_results
    
    
    def _generate_comparison_table(self, all_results):
        """Generate comparison table across all routers"""
        print("\n" + "=" * 80)
        print(" COMPARISON TABLE")
        print("=" * 80 + "\n")
        
        if not all_results:
            print("No results to compare.")
            return
        
        # Header
        print(f"{'Category':<25} {'Simple':<15} {'Gemini':<15} {'GPT-4':<15}")
        print("-" * 80)
        
        # Overall accuracy
        print(f"{'OVERALL ACCURACY':<25}", end="")
        for mode in ['simple', 'gemini', 'gpt']:
            if mode in all_results:
                acc = all_results[mode]['overall']['accuracy']
                print(f"{acc:>6.1f}%{' '*8}", end="")
            else:
                print(f"{'N/A':<15}", end="")
        print()
        
        print("-" * 80)
        
        # Category breakdown
        categories = ['basic', 'edge_cases', 'clinical_safety', 'hallucination', 'uncertainty']
        category_names = {
            'basic': 'Basic Routing',
            'edge_cases': 'Edge Cases',
            'clinical_safety': 'Clinical Safety',
            'hallucination': 'Hallucination Tests',
            'uncertainty': 'Uncertainty Handling'
        }
        
        for category in categories:
            print(f"{category_names[category]:<25}", end="")
            for mode in ['simple', 'gemini', 'gpt']:
                if mode in all_results and category in all_results[mode]['categories']:
                    acc = all_results[mode]['categories'][category]['accuracy']
                    print(f"{acc:>6.1f}%{' '*8}", end="")
                else:
                    print(f"{'N/A':<15}", end="")
            print()
        
        print("-" * 80)
        
        # Performance metrics
        print(f"{'Avg Response Time':<25}", end="")
        for mode in ['simple', 'gemini', 'gpt']:
            if mode in all_results:
                time_val = all_results[mode]['overall']['avg_response_time']
                print(f"{time_val:>6.3f}s{' '*7}", end="")
            else:
                print(f"{'N/A':<15}", end="")
        print()
        
        print("=" * 80 + "\n")
    
    
    def _generate_detailed_report(self, all_results):
        """Generate detailed markdown report"""
        report_path = 'evaluation/results.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# LLM Router Evaluation Results\n\n")
            f.write(f"**Evaluation Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Project:** Nordhealth AI Engineer Intern Assignment\n\n")
            f.write(f"**Author:** Ata Jodeiri Seyedian\n\n")
            f.write("---\n\n")
            
            # Executive Summary
            f.write("## Executive Summary\n\n")
            f.write(f"This evaluation tested **{sum(len(tests) for tests in self.test_data.values())} queries** ")
            f.write("across **5 categories** to compare three routing approaches:\n\n")
            f.write("1. **Simple Rule-Based Router** - Baseline using keyword matching\n")
            f.write("2. **Google Gemini (gemini-2.5-flash)** - LLM-powered routing\n")
            f.write("3. **Azure OpenAI (GPT-4o)** - Premium LLM-powered routing\n\n")
            
            # Overall Results Table
            f.write("## Overall Results\n\n")
            f.write("| Router | Total Queries | Correct | Accuracy | Avg Response Time |\n")
            f.write("|--------|--------------|---------|----------|------------------|\n")
            
            for mode in ['simple', 'gemini', 'gpt']:
                if mode in all_results:
                    r = all_results[mode]['overall']
                    mode_name = {'simple': 'Simple', 'gemini': 'Gemini', 'gpt': 'GPT-4'}[mode]
                    f.write(f"| {mode_name} | {r['total_queries']} | {r['correct']} | ")
                    f.write(f"{r['accuracy']:.1f}% | {r['avg_response_time']:.3f}s |\n")
            
            f.write("\n")
            
            # Category Breakdown
            f.write("## Category Breakdown\n\n")
            
            categories = ['basic', 'edge_cases', 'clinical_safety', 'hallucination', 'uncertainty']
            category_names = {
                'basic': 'Basic Routing',
                'edge_cases': 'Edge Cases',
                'clinical_safety': 'Clinical Safety',
                'hallucination': 'Hallucination Detection',
                'uncertainty': 'Uncertainty Handling'
            }
            
            for category in categories:
                f.write(f"### {category_names[category]}\n\n")
                f.write("| Router | Queries | Correct | Accuracy | Avg Time |\n")
                f.write("|--------|---------|---------|----------|----------|\n")
                
                for mode in ['simple', 'gemini', 'gpt']:
                    if mode in all_results and category in all_results[mode]['categories']:
                        c = all_results[mode]['categories'][category]
                        mode_name = {'simple': 'Simple', 'gemini': 'Gemini', 'gpt': 'GPT-4'}[mode]
                        f.write(f"| {mode_name} | {c['total']} | {c['correct']} | ")
                        f.write(f"{c['accuracy']:.1f}% | {c['avg_response_time']:.3f}s |\n")
                
                f.write("\n")
            
            # Error Analysis
            f.write("## Error Analysis\n\n")
            
            for mode in ['simple', 'gemini', 'gpt']:
                if mode not in all_results:
                    continue
                
                mode_name = {'simple': 'Simple', 'gemini': 'Gemini', 'gpt': 'GPT-4'}[mode]
                f.write(f"### {mode_name} Router Errors\n\n")
                
                has_errors = False
                for category in categories:
                    if category in all_results[mode]['categories']:
                        errors = all_results[mode]['categories'][category].get('errors', [])
                        if errors:
                            has_errors = True
                            f.write(f"**{category_names[category]}:**\n\n")
                            for error in errors[:5]:  # Show first 5 errors
                                f.write(f"- Query: \"{error['query'][:80]}...\"\n")
                                f.write(f"  - Expected: `{error['expected']}`\n")
                                f.write(f"  - Actual: `{error['actual']}`\n\n")
                
                if not has_errors:
                    f.write("No errors detected!\n\n")
                else:
                    f.write("\n")
            
            # Recommendation
            f.write("## Recommendation\n\n")
            
            # Find best router
            best_mode = max(all_results.keys(), 
                          key=lambda m: all_results[m]['overall']['accuracy'])
            best_name = {'simple': 'Simple', 'gemini': 'Gemini', 'gpt': 'GPT-4'}[best_mode]
            best_acc = all_results[best_mode]['overall']['accuracy']
            
            f.write(f"**Recommended for Production: {best_name} Router**\n\n")
            f.write(f"- **Accuracy:** {best_acc:.1f}%\n")
            f.write(f"- **Response Time:** {all_results[best_mode]['overall']['avg_response_time']:.3f}s\n")
            
            if best_mode == 'gemini':
                f.write("- **Cost:** Free (Google Gemini API)\n")
                f.write("- **Justification:** Best balance of accuracy, speed, and cost-effectiveness\n\n")
            elif best_mode == 'gpt':
                f.write("- **Cost:** ~$0.50 per 1,000 queries\n")
                f.write("- **Justification:** Highest accuracy, acceptable speed, reasonable cost with Azure credits\n\n")
            else:
                f.write("- **Cost:** $0 (no API calls)\n")
                f.write("- **Justification:** Instant response, no dependencies, good for baseline\n\n")
        
        print(f"Detailed report saved to: {report_path}\n")


def main():
    """Main evaluation function"""
    evaluator = RouterEvaluator()
    
    # Run comparison
    results = evaluator.compare_routers(modes=['simple', 'gemini', 'gpt'])
    
    print("\n" + "=" * 80)
    print("EVALUATION COMPLETE!")
    print("=" * 80)
    print("\nResults saved to:")
    print("  evaluation/results.md - Detailed markdown report")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()