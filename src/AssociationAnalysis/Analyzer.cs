using System;
using System.Linq;
using AssociationAnalysis.Apriori;
using AssociationAnalysis.Properties;

namespace AssociationAnalysis
{
    public class Analyzer
    {
        public static void Main(string[] args)
        {
            var dataSet = new DataSet(Resources.msnbc990928);
            dataSet.DataHeaders.ToList()
                               .ForEach(
                                            u => Console.WriteLine("{0}:{1}", u.Key, u.Value)
                                       );

            Apriori(dataSet);

            Console.ReadLine(); //Stop program so we can read output
        }

        private static void Apriori(DataSet data)
        {
            bool verbose = true;
            var cData = new CompactDataSet(data) { Verbose = verbose };
            var miner = new AprioriMiner(cData) { MinSupport = 0.01, MinConfidence = 0.3, Verbose = verbose };
            cData.printInfo();
            miner.mine();
        }
    }
}
