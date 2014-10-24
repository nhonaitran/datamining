using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
using System.Text;
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
        }
    }
}
