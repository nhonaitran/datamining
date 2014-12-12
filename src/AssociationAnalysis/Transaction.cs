using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AssociationAnalysis {
    public class Transaction {
        public int ID { get; set; }
        public IEnumerable<Item> Itemset { get; set; }
        public string Description { get; set; }
    }
}
