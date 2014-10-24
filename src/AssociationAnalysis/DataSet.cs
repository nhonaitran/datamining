using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace AssociationAnalysis
{
    public class DataSet
    {
        public IEnumerable<string[]> SequentialData { get; set; }
        public IEnumerable<IEnumerable<string>> AssociationData { get; set; }
        public Dictionary<int, string> DataHeaders { get; set; }
        public DataSet(byte[] p)
        {// parse file
            var rawData = Encoding.Default
                               .GetString(p)
                               .Split('\n')
                               .Where(d => !d.Contains("%") && d.Trim().Length > 0)
                               .ToList();
            // header data key map
            DataHeaders = new Dictionary<int, string>();
            var i = 1;
            // fill key map
            rawData[0].Split(' ').ToList().ForEach(u => DataHeaders.Add(i++, u));
            // remove headers from raw data
            rawData.RemoveAt(0);

            SequentialData = rawData.Select(u => u.Split(' '));
            AssociationData = rawData.Select(u => u.Split(' ').Distinct());
        }
    }
}
