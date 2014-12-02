using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AssociationAnalysis.KSequence
{
    public class KSequenceMiner
    {
        public KSequenceMiner()
        {
            Rules = new Dictionary<string, int>();
        }

        public bool FilterRepeatedNavigations { get; set; }
        public DataSet DataSet { get; set; }
        public int K { get; set; }
        public double MinimumSupport { get; set; }
        private double supportDenominator { get; set; }
        private readonly Dictionary<string, int> Rules;
        private static void addToDictionary(string s, Dictionary<string, int> d, int i)
        {
            if (d.ContainsKey(s))
            {
                d[s] += i;
            }
            else
            {
                d.Add(s, i);
            }
        }

        public void Mine()
        {
            var sequencesWithAtLeastKNodes = DataSet.SequentialData.Where(d => d.Count() > K - 1).ToList(); // all sequences of at least length k
            var distinctSequences = FilterRepeatedNavigations ? GetDistinctSequences(sequencesWithAtLeastKNodes)
                                                              : sequencesWithAtLeastKNodes;

            supportDenominator = 0;
            var tempRules = new Dictionary<string, int>();
            var navigationPattern = new Queue<char>(K);

            foreach (var nodeSequence in distinctSequences)
            {
                navigationPattern.Clear();
                foreach (var node in nodeSequence)
                {
                    navigationPattern.Enqueue(((char)(node + 64)));
                    if (navigationPattern.Count < K) continue;
                    addToDictionary(string.Join("", navigationPattern.ToArray()), tempRules, 1);
                    navigationPattern.Dequeue();
                    supportDenominator++;
                }
            }

            //remove candidate rules that do not have required support
            foreach (var supCount in tempRules.Where(supCount => supCount.Value / (double)supportDenominator >= MinimumSupport))
            {
                addToDictionary(supCount.Key, Rules, supCount.Value);
            }
            PrintRules();
        }

        private IEnumerable<IEnumerable<int>> GetDistinctSequences(IEnumerable<IEnumerable<int>> sequencesWithAtLeastKNodes)
        {
            var distinctSequences = new List<IEnumerable<int>>();
            foreach (var nodeSequence in sequencesWithAtLeastKNodes)
            {
                var prevNode = 0;
                var newSequence = new List<int>();
                foreach (var node in nodeSequence)
                {
                    if (prevNode != node)
                    {
                        newSequence.Add(node);
                    }
                    prevNode = node;
                }
                if (newSequence.Count() > K)
                {
                    distinctSequences.Add(newSequence);
                }
            }
            return distinctSequences;
        }

        private void PrintRules()
        {
            var ruleList = Rules.ToList();
            ruleList.Sort((firstPair, nextPair) => firstPair.Value.CompareTo(nextPair.Value));
            ruleList.Reverse();

            foreach (var supCount in ruleList)
            {
                var sb = new StringBuilder();
                foreach (var j in supCount.Key.Select(c => c - 64))
                {
                    sb.Append(DataSet.DataHeaders[j] + " ~> ");
                }
                Console.WriteLine("The rule: {0} has a support of {1}%.", sb.ToString().Trim(" ~> ".ToCharArray()), (supCount.Value * 100 / supportDenominator).ToString().Substring(0, 4));
            }
        }

    }
}
