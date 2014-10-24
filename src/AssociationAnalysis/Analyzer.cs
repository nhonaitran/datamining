using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using AssociationAnalysis.Properties;

namespace AssociationAnalysis
{
    public class Analyzer
    {
        public static void Main(string[] args)
        {
            var data = Encoding.Default
                               .GetString(Resources.msnbc990928)
                               .Split('\n')
                               .Where(d => !d.Contains("%") && d.Trim().Length > 0)
                               .ToList();
        }
    }
}
