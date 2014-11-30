using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AssociationAnalysis.Apriori
{
    /// <summary>
    /// A compact data set. Data is grouped by number of items and stored as a bit field. Each element also has a support count for all of the times it appears in the original data set.
    /// Data Dictionary Structure: Set Length -> (Data Bitfield -> Support count)
    /// </summary>
    class CompactDataSet
    {
        public bool Verbose { get; set; }
        
        public Dictionary<int, Dictionary<uint, int>> Data { get; private set; }
        public int Size { get; private set; }
        public Dictionary<int, string> Headers { get; private set; }

        public CompactDataSet(DataSet origData) : this(origData, true) { }

        public CompactDataSet(DataSet origData, bool verbose)
        {
            Verbose = verbose;
            Headers = origData.DataHeaders;
            Data = new Dictionary<int, Dictionary<uint, int>>();
            Size = 0;

            if (Verbose) { Console.Write("Compacting Data: 0..."); }

            compact(origData.AssociationData);

            if (Verbose) { Console.WriteLine(); }
        }

        /// <summary>
        /// Compact the original data set into the new length segregated, binzarized, no-duplicate data structure.
        /// </summary>
        /// <param name="origData">The orinal data stream.</param>
        private void compact(IEnumerable<IEnumerable<int>> origData)
        {
            int iteration = 1;
            foreach (var elem in origData)
            {
                if (Verbose && iteration % 10000 == 0)
                    Console.Write("\rCompacting Data: " + iteration + "... ");

                uint bElem = binarize(elem);

                int len = elem.Count();
                if (!Data.ContainsKey(len)) //Data of this length has not been encountered yet
                {
                    var dict = new Dictionary<uint, int>();
                    dict.Add(bElem, 1); //Length has not been encountered, so we have not seen this element yet
                    Data[len] = dict;
                }
                else
                {
                    var dict = Data[len];
                    bool match = false;
                    foreach (uint key in dict.Keys)
                    {
                        if (key == bElem) //Current element is a duplicate, simply increase support
                        {
                            dict[key] += 1;
                            match = true;
                            break;
                        }
                    }

                    if (!match) //Current element has not been seen yet
                    {
                        dict.Add(bElem, 1);
                    }
                }

                iteration++;
            }

            Size = iteration;
            if (Verbose)
                Console.Write("\rCompacting Data: " + iteration + "... Done");
        }

        /// <summary>
        /// Compute the support count for an item set of length len.
        /// Setting len=1 will compare against everything, but is inefficient.
        /// </summary>
        /// <param name="bElem">The item set to calculate the support count for.</param>
        /// <param name="len">The number of items in bElem.</param>
        /// <returns>The support count for bElem.</returns>
        public int calcSupport(uint bElem, int len)
        {
            int supportCount = 0;
            foreach (int key in Data.Keys.Where(n => n >= len).OrderBy(n => n))
            {
                foreach (uint currentElem in Data[key].Keys)
                {
                    if (isSubset(bElem, currentElem))
                        supportCount += Data[key][currentElem];
                }
            }
            return supportCount;
        }

        /// <summary>
        /// Compute the interest (lift) measure for the rule X -> Y.
        /// </summary>
        /// <param name="x">The antecedent itemset.</param>
        /// <param name="lenx">The size of the antecedent itemset. (Can default to 1, but results in more comparisons)</param>
        /// <param name="y">The consequent itemset.</param>
        /// <param name="leny">The size of the consequent itemset. (Can default to 1, but results in more comparisons)</param>
        /// <returns>The interest (lift) measure for the rule X -> Y.</returns>
        public double calcInterest(uint x, int lenx, uint y, int leny)
        {
            return calcConfidence(x, lenx, y, leny) / ((double)calcSupport(y, leny) / (double)Size);
        }

        /// <summary>
        /// Compute the confidence measure for the rule X -> Y.
        /// </summary>
        /// <param name="x">The antecedent itemset.</param>
        /// <param name="lenx">The size of the antecedent itemset. (Can default to 1, but results in more comparisons)</param>
        /// <param name="y">The consequent itemset.</param>
        /// <param name="leny">The size of the consequent itemset. (Can default to 1, but results in more comparisons)</param>
        /// <returns>The confidence measure for the rule X -> Y.</returns>
        public double calcConfidence(uint x, int lenx, uint y, int leny)
        {
            return calcSupport(x | y, Math.Min(lenx, leny)) / ((double)calcSupport(x, lenx));
        }

        /// <summary>
        /// Convert a list of distinct integers (all elements between 1 and 32) into a bit field.
        /// </summary>
        /// <param name="element">A list of distinct integers (elements between 1 and 32)</param>
        /// <returns>A uint bitfield representing the list</returns>
        public static uint binarize(IEnumerable<int> element)
        {
            uint bElem = 0;
            foreach (int item in element)
            {
                bElem += 1U << (item - 1);
            }
            return bElem;
        }

        /// <summary>
        /// Convert a bit field into a list of distinct integers representing each bit.
        /// </summary>
        /// <param name="bElem">A bitfield representing a list of distinct integers.</param>
        /// <returns>The list obtained from the bitfield.</returns>
        public static IList<int> unbinarize(uint bElem)
        {
            var elem = new List<int>();
            for (int i = 0; i < 32; i++)
            {
                uint mask = 1U << i;
                if ((bElem & mask) != 0)
                    elem.Add(i + 1);
            }
            return elem;
        }

        /// <summary>
        /// Convert a bit field into a list of headers, where a header is the string represented by a bit in the bit field.
        /// </summary>
        /// <param name="bElem">A bitfield representing a list of distinct integers.</param>
        /// <returns>The list of headers obtained from the bitfield.</returns>
        public IEnumerable<string> asHeaders(uint bElem)
        {
            return unbinarize(bElem).Select(u => Headers[u]);
        }

        /// <summary>
        /// Is A a subset of B?
        /// </summary>
        /// <param name="A">A bit field representing an element.</param>
        /// <param name="B">A bit field representing an element.</param>
        /// <returns>true if A is a subset of B.</returns>
        public static bool isSubset(uint A, uint B)
        {
            return (A | B) == B;
        }

        /// <summary>
        /// Print broad information about the segregated data set.
        /// </summary>
        public void printInfo()
        {
            foreach (int len in Data.Keys.OrderBy(x => x))
            {
                int nDistElem = Data[len].Values.Count();
                int nElem = 0;
                foreach (var kvPair in Data[len])
                {
                    nElem += kvPair.Value;
                }

                Console.WriteLine("Len " + len + ": " + nDistElem + " distinct elements (" + nElem + " total elements / " + Size + ")");
            }
        }
    }
}
