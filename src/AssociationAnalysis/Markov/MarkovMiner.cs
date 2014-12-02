using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AssociationAnalysis.Markov
{
    class MarkovMiner
    {
        public DataSet DataSet { get; set; }
        public int[,] VisitMatrix { get; set; }
        public void Mine()
        {
            var previousNode = 0;
            var nonDistinctNavigations = DataSet.SequentialData.Where(d => d.Count() > 1);
            VisitMatrix = new int[DataSet.DataHeaders.Count + 1, DataSet.DataHeaders.Count + 1];

            foreach (var node in nonDistinctNavigations.SelectMany(navigationList => navigationList))
            {
                VisitMatrix[previousNode, node]++;
                previousNode = node;
            }
            Print();
        }

        private void Print()
        {
            var stringBuilder = new StringBuilder();
            for (var i = 1; i < DataSet.DataHeaders.Count + 1; i++)
            {
                for (var j = 1; j < DataSet.DataHeaders.Count + 1; j++)
                {
                    stringBuilder.Append(VisitMatrix[i, j] + ",");
                }
                Console.WriteLine(stringBuilder.ToString().Trim(','));
                stringBuilder.Clear();
            }
        }
    }
}
