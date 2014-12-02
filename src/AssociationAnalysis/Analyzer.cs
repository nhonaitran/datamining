using System;
using System.Collections.Generic;
using System.Data.Common;
using System.Diagnostics;
using System.Linq;
using System.Text;
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
            // Apriori(dataSet);
            // Markov(dataSet);

            Console.ReadLine(); //Stop program so we can read output
        }

        private static void Apriori(DataSet data)
        {
            Stopwatch stopwatch = new Stopwatch(); 
            stopwatch.Start();
            bool verbose = true;
            var cData = new CompactDataSet(data) { Verbose = verbose };
            var miner = new AprioriMiner(cData) { MinSupport = 0.01, MinConfidence = 0.3, Verbose = verbose };
            cData.printInfo();
            miner.mine();
            stopwatch.Stop();
            TimeSpan ts = stopwatch.Elapsed;

            //Format and display the TimeSpan value. 
            string elapsedTime = String.Format("{0:00}:{1:00}:{2:00}.{3:00}",
                ts.Hours, ts.Minutes, ts.Seconds,
                ts.Milliseconds / 10);
            Console.WriteLine("Apriori RunTime: " + elapsedTime);
        }

        private static void Markov(DataSet data)
        {
            var previousNode = 0;
            var nonDistinctNavigations = data.SequentialData.Where(d => d.Count() > 1);
            var visitMatrix = new int[data.DataHeaders.Count + 1, data.DataHeaders.Count + 1];

            foreach (var node in nonDistinctNavigations.SelectMany(navigationList => navigationList))
            {
                visitMatrix[previousNode, node]++;
                previousNode = node;
            }

            var stringBuilder = new StringBuilder();

            for (var i = 1; i < data.DataHeaders.Count + 1; i++)
            {
                for (var j = 1; j < data.DataHeaders.Count + 1; j++)
                {
                    stringBuilder.Append(visitMatrix[i, j] + ",");
                }
                Console.WriteLine(stringBuilder.ToString().Trim(','));
                stringBuilder.Clear();
            }
        }
    }
}
