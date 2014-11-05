using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace AssociationAnalysis
{
    public class DataSet
    {
        public int NumberOfTransactions { get; set; }
        public int NumberOfItems { get; set; }
        public IEnumerable<IEnumerable<int>> SequentialData { get; set; }
        public IEnumerable<IEnumerable<int>> AssociationData { get; set; }
        public Dictionary<int, string> DataHeaders { get; set; }

        public int[][] AssociationDataBinaryFormat { get; set; }
        
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
            NumberOfItems = DataHeaders.Count;

            char[] separators = {' ', '\r'}; //carriage returns and extra space are at the end of every line
            SequentialData = rawData.Select(u => u.Split(separators, StringSplitOptions.RemoveEmptyEntries).Select(int.Parse));
            AssociationData = rawData.Select(u => u.Split(separators, StringSplitOptions.RemoveEmptyEntries).Select(int.Parse).Distinct().OrderBy(x => x));
            NumberOfTransactions = rawData.Count;
        }

        public void CreateBinaryRepresentation() {
            AssociationDataBinaryFormat = new int[NumberOfTransactions][];
            int i = 0;
            AssociationData.ToList().ForEach(t => { 
                AssociationDataBinaryFormat[i] = new int[NumberOfItems];  
                t.ToList().ForEach(j => AssociationDataBinaryFormat[i][j - 1] = 1); 
                i++; 
            });
        }

        public void SaveBinaryRepresentation(string filename) {
            using (System.IO.StreamWriter file = new System.IO.StreamWriter(filename)) {
                file.WriteLine(string.Join(",", DataHeaders.Values));
                AssociationDataBinaryFormat.ToList().ForEach(t => file.WriteLine(string.Join(",", t.ToList())));
            }
        }
    }
}
