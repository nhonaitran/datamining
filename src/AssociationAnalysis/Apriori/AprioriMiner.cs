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
        }
    }
}
