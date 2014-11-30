using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AssociationAnalysis.Apriori
{
    /// <summary>
    /// Performs Apriori Association mining
    /// </summary>
    class AprioriMiner
    {
        private CompactDataSet DataSet;
        public bool Verbose { get; set; }

        private double _MinSupport = 0;
        /// <summary>
        /// Value in [0,1] for the percent of data needed for an itemset to be considered 'frequent'.
        /// </summary>
        public double MinSupport
        {
            get
            {
                return _MinSupport;
            }
            set
            {
                if (value < 0 || value > 1) throw new ArgumentOutOfRangeException("MinSupport", "MinSupport must be in the interval [0,1].");
                else this._MinSupport = value;
            }
        }

        private double _MinConfidence = 0;
        /// <summary>
        /// Value in [0,1] for the minimum confidence measure a rules needs to not be pruned.
        /// </summary>
        public double MinConfidence
        {
            get
            {
                return _MinConfidence;
            }
            set
            {
                if (value < 0 || value > 1) throw new ArgumentOutOfRangeException("MinConfidence", "MinConfidence must be in the interval [0,1].");
                else this._MinConfidence = value;
            }
        }

        /// <summary>
        /// Create a new Apriori Miner
        /// </summary>
        /// <param name="DataSet">The data set to mine.</param>
        public AprioriMiner(CompactDataSet DataSet)
        {
            this.DataSet = DataSet;
        }

        /// <summary>
        /// Perform association mining.
        /// </summary>
        public void mine()
        {
            var freqItemSets = generateItemSets();
            
            if (Verbose)
            {
                Console.WriteLine("Frequent Item Sets (" + MinSupport * 100 + "% Min Support): ");
                foreach (int key in freqItemSets.Keys.OrderBy(n => n))
                    foreach (uint bElem in freqItemSets[key].OrderBy(n => n))
                    {
                        Console.WriteLine("\t" + String.Join(", ", DataSet.asHeaders(bElem)));
                    }
            }

            var rules = generateRules(freqItemSets);

            if (Verbose)
            {
                Console.WriteLine("Generated Rules (" + MinConfidence * 100 + "% Min Confidence): ");
                foreach (var rule in rules)
                {
                    var ante = String.Join(", ", DataSet.asHeaders(rule.Antecedant));
                    var conq = String.Join(", ", DataSet.asHeaders(rule.Consequent));
                    Console.WriteLine("\t" + ante + " -> " + conq + "\t Conf=" + string.Format("{0:0.0000}", rule.Confidence) + "\t Lift=" + string.Format("{0:0.0000}", rule.Lift));
                }
            }
        }

        /// <summary>
        /// Generates frequent itemsets.
        /// </summary>
        /// <returns>A dictionary of frequent itemsets. Keys are set size, and values are frequent sets of that size.</returns>
        private Dictionary<int, IList<uint>> generateItemSets()
        {
            var freqItemSets = new Dictionary<int, IList<uint>>();
            int minSupportCount = (int)(_MinSupport * DataSet.Size);

            //Initialize with length 1 frequent item sets.
            freqItemSets[1] = new List<uint>();
            foreach (uint bElem in DataSet.Data[1].Keys)
            {
                if (DataSet.calcSupport(bElem, 1) >= minSupportCount)
                    freqItemSets[1].Add(bElem);
            }

            //Generate larger frequent itemsets.
            for (int len = 2; len <= 32; len++)
            {
                var newItemSet = new List<uint>();
                var oldItemSet = freqItemSets[len - 1];
                //Compare each of the size len-1 itemsets against each other.
                for (int i = 0; i < oldItemSet.Count() - 1; i++)
                {
                    for (int j = i + 1; j < oldItemSet.Count(); j++)
                    {
                        uint bElem1 = oldItemSet[i];
                        uint bElem2 = oldItemSet[j];
                        if (shouldCombine(bElem1, bElem2, len - 2))
                            newItemSet.Add(bElem1 | bElem2); //Combine the smaller itemsets
                    }
                }

                //Filter entries that do not have minimum support.
                newItemSet = newItemSet
                    .Distinct()
                    .Where(bElem => DataSet.calcSupport(bElem, len) >= minSupportCount)
                    .ToList();

                if (newItemSet.Count() == 0) //Stop generating new itemsets
                    break;
                else
                    freqItemSets[len] = newItemSet;
            }

            return freqItemSets;
        }

        /// <summary>
        /// Tests to see if the first len items in an item set match.
        /// If so, we know we can combine the two elements to form a new itemset.
        /// </summary>
        /// <param name="bElem1">The first item set.</param>
        /// <param name="bElem2">The second item set.</param>
        /// <param name="len">The number of items that must match.</param>
        /// <returns>true if the first len elements match, false otherwise</returns>
        private bool shouldCombine(uint bElem1, uint bElem2, int len)
        {
            int matched = 0;
            for (int i = 0; matched < len && i < 32; i++)
            {
                uint mask = 1U << i;
                uint lhs = mask & bElem1, rhs = mask & bElem2; //Check the ith bit of each item set
                if (lhs == rhs)
                {
                    if (lhs != 0) //We have a 11 match, not a 00 match.
                        matched++;
                }
                else
                    return false; //The ith bit is not equal.
            }

            return matched == len; //If matched != len, then one itemset was somehow bigger than the other.
        }

        /// <summary>
        /// Generate all rules from frequent itemsets with at least the minimum required confidence.
        /// </summary>
        /// <param name="freqItemSets">The frequent item sets to generate rules from.</param>
        /// <returns>All rules from frequent itemsets with at least the minimum required confidence.</returns>
        private IList<AssociationRule> generateRules(Dictionary<int, IList<uint>> freqItemSets)
        {
            var rules = new List<AssociationRule>();
            foreach (int size in freqItemSets.Keys.OrderBy(n => n).Where(n => n >= 2))
            {
                foreach (uint bElem in freqItemSets[size])
                {
                    //Get rules with size 1 consequents
                    var startRules = generateSingleConsequentRulesFromItemSet(bElem, size);
                    rules.AddRange(startRules);

                    //Genereate rules with larger consequents
                    for (int conqSize = 2; conqSize < size && startRules.Count > 1; conqSize++)
                    {
                        var newRules = new List<AssociationRule>();

                        //Iterate over pairs of rules with conqSize-1 size consequents.
                        for (int i = 0; i < startRules.Count - 1; i++)
                            for (int j = i + 1; j < startRules.Count; j++)
                            {
                                AssociationRule rule1 = startRules[i], rule2 = startRules[j];
                                if (shouldCombine(rule1.Consequent, rule2.Consequent, conqSize - 2)) //Should we combine the consequents?
                                {
                                    uint conq = rule1.Consequent | rule2.Consequent; //Form new merged consequent.
                                    var rule = new AssociationRule(bElem & ~conq, size - conqSize, conq, conqSize, DataSet);
                                    if (rule.Confidence >= MinConfidence) //Accept the rule if it meets required threshold.
                                        newRules.Add(rule);
                                }
                            }

                        rules.AddRange(newRules);
                        startRules = newRules; //We will generate the next round of rules from the rules generated this round.
                    }   
                }
            }
            return rules;
        }

        /// <summary>
        /// Generate rules from an item set where the rules have a size 1 consequent.
        /// Only rules with confidence at least MinConfidence will be returned.
        /// </summary>
        /// <param name="bElem">The frequent item set to generate rules from</param>
        /// <param name="size">The size of the frequent item set.</param>
        /// <returns>Rules of the form Y-X -> X where Y is the item set, |X|=1, and confidence(Y-X -> X) >= MinConfidence.</returns>
        private IList<AssociationRule> generateSingleConsequentRulesFromItemSet(uint bElem, int size)
        {
            var rules = new List<AssociationRule>();
            for (int i = 0; i < 32; i++) //32 bits in uint
            {
                uint mask = 1U << i;
                if ((bElem & mask) != 0)
                {
                    var rule = new AssociationRule(bElem & ~mask, size - 1, mask, 1, DataSet);
                    if (rule.Confidence >= MinConfidence)
                        rules.Add(rule);
                }
            }
            return rules;
        }
    }
}
