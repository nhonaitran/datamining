using System;
using System.Collections.Generic;
using System.IO;
using NUnit.Framework;
using AssociationAnalysis.Tests.Properties;

namespace AssociationAnalysis.Tests
{
    [TestFixture]
    public class DataSetTests
    {
        DataSet data;
        static int itemPresent = 1;
        string filename = Environment.CurrentDirectory + "\\test.csv";

        [SetUp]
        public void Init() {
            data = new DataSet(Resources.test);
        }

        [Test]
        public void TestAssociationDataConvertedToBinaryRepresentation() {
            data.CreateBinaryRepresentation();
            Assert.AreEqual(itemPresent, data.AssociationDataBinaryFormat[0][0]);
            Assert.AreEqual(itemPresent, data.AssociationDataBinaryFormat[1][1]);
            Assert.AreEqual(itemPresent, data.AssociationDataBinaryFormat[2][1]);
            Assert.AreEqual(itemPresent, data.AssociationDataBinaryFormat[2][2]);
            Assert.AreEqual(itemPresent, data.AssociationDataBinaryFormat[2][3]);
            Assert.AreEqual(itemPresent, data.AssociationDataBinaryFormat[3][4]);
            Assert.AreEqual(itemPresent, data.AssociationDataBinaryFormat[4][0]);
            Assert.AreEqual(itemPresent, data.AssociationDataBinaryFormat[5][5]);
            Assert.AreEqual(itemPresent, data.AssociationDataBinaryFormat[6][0]);
        }

        [Test]
        public void TestSaveBinaryRepresentationToFile() {
            data.CreateBinaryRepresentation();

            if (File.Exists(filename)) File.Delete(filename);
            data.SaveBinaryRepresentation(filename);

            Assert.AreEqual(File.ReadAllText(filename), Resources.test_data_binary_representation);
        }

        [Test]
        public void TestSaveEntireRawDataFile() {
            var processedData = new DataSet(AssociationAnalysis.Properties.Resources.msnbc990928);
            processedData.CreateBinaryRepresentation();
            processedData.SaveBinaryRepresentation(Environment.CurrentDirectory + "\\WebUsage.raw.csv");
        }

        [TearDown]
        public void CleanUp() {
            if (File.Exists(filename)) File.Delete(filename);            
        }
    }
}
