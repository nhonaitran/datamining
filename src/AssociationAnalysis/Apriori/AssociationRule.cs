using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AssociationAnalysis.Apriori
{
    /// <summary>
    /// Bundles together the antecedent and consequennt of a rule along with its confidence and lift metrics.
    /// </summary>
    class AssociationRule
    {
        public uint Antecedant { get; private set; }
        public uint Consequent { get; private set; }
        public double Confidence { get; private set; }
        public double Lift { get; private set; }

        /// <summary>
        /// Createa new association rule and calculate its confidence and lift metrics on the given data set.
        /// </summary>
        /// <param name="ante">The binarized element X, of X -> Y</param>
        /// <param name="anteSize">The size of X</param>
        /// <param name="conq">The binarized element Y, of X -> Y</param>
        /// <param name="conqSize">The size of Y</param>
        /// <param name="DataSet">The data set to use to calculate metrics.</param>
        public AssociationRule(uint ante, int anteSize, uint conq, int conqSize, CompactDataSet DataSet)
        {
            Antecedant = ante;
            Consequent = conq;
            Confidence = DataSet.calcConfidence(ante, anteSize, conq, conqSize);
            Lift = DataSet.calcInterest(ante, anteSize, conq, conqSize);
        }
    }
}
