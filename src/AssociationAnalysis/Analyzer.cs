using System;
using System.Collections.Generic;
using System.Data.Common;
using System.Diagnostics;
using System.Linq;
using System.Text;
using AssociationAnalysis.Apriori;
using AssociationAnalysis.KSequence;
using AssociationAnalysis.Markov;
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
            /*
               KSequence(dataSet, 3, .01, true);
               Console.WriteLine("-----");
               KSequence(dataSet, 3, .01, false);
            */

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
            (new MarkovMiner() { DataSet = data }).Mine();
        }

        private static void KSequence(DataSet data, int k, double minimumSupport, bool filterRepeatedNavigations = true)
        {
            (new KSequenceMiner
            {
                DataSet = data,
                FilterRepeatedNavigations = filterRepeatedNavigations,
                K = k,
                MinimumSupport = minimumSupport
            }).Mine();
        }
    }
}
