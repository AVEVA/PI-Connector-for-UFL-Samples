using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace DataDefinitionInDifferentFileINIGenerator
{
    class Program
    {
        static StringBuilder iniContent = new StringBuilder();
        static string iniFilePath = "DataDefinitionInDifferentFile.ini";

        static string dataDefinitionFilePath = @"DataDefinitionInDifferentFile.definition";
        static int dataDefinitionFileRowStart = 3; // included
        static int dataDefinitionFileRowStop = 23; // included
        static List<DataDefinitionItem> dataDefinitionItems = new List<DataDefinitionItem>();

        static string dataCollector = "";
        static int count = 0;

        static void Main(string[] args)
        {
            LoadDataDefinition();

            GenerateFIELD();
            GenerateMSG();
            GenerateDataMSGType();

            CreateINIFile();
        }

        private static void LoadDataDefinition()
        {
            count = 0;
            int rowN = 0;
            if (!File.Exists(dataDefinitionFilePath))
            {
                Console.WriteLine("Invalid data definition path.");
                Environment.Exit(0);
            }
            using (var streamReader = new StreamReader(dataDefinitionFilePath))
            {
                string line = "";
                while ((line = streamReader.ReadLine()) != null)
                {
                    ++rowN;

                    if (rowN == 1)
                        dataCollector = line;


                    if (rowN >= dataDefinitionFileRowStart && rowN <= dataDefinitionFileRowStop)
                    {
                        ++count;
                        string[] parts = line.Split(';');
                        dataDefinitionItems.Add(new DataDefinitionItem(parts[0], parts[1], parts[2]));
                        //Console.WriteLine(count + parts[0] + parts[1] + parts[2]);
                    }
                }
            }
        }

        private static void GenerateFIELD()
        {
            iniContent.AppendLine(
                "[FIELD]\r\n" +
                "FIELD(1).Name = \"DynAttrCol\"\r\n" +
                "FIELD(1).Type = \"Collection\"\r\n" +
                "FIELD(2).Name = \"StatAttrCol\"\r\n" +
                "FIELD(2).Type = \"Collection\"\r\n" +
                "FIELD(3).NAME = \"Timestamp\"\r\n" +
                "FIELD(3).TYPE = \"DateTime\"\r\n" +
                "FIELD(3).FORMAT = \"dd-MM-yyyyhh:mm:ss.nnn\"\r\n" +
                "FIELD(4).NAME = \"TSDateString\"\r\n" +
                "FIELD(5).NAME = \"TSTimeString\"\r\n");

            int fieldN = 10;

            foreach (DataDefinitionItem ddi in dataDefinitionItems)
            {
                iniContent.AppendLine(
                    "FIELD(" + fieldN + ").NAME = \"Value" + (fieldN - 9) + "Number\"\r\n" +
                    "FIELD(" + fieldN + ").TYPE = \"Number\"");
                ++fieldN;
            }

        }

        private static void GenerateMSG()
        {
            iniContent.AppendLine(
                "\r\n[MSG]\r\n" +
                "MSG(1).NAME=\"Data\"\r\n");
        }

        private static void GenerateDataMSGType()
        {
            iniContent.AppendLine(
                "[Data]\r\n" +
                "Data.FILTER = C1 == \"##-*\"\r\n" +
                "DynAttrCol = Clear()\r\n" +
                "StatAttrCol = Clear()\r\n" +
                "__MESSAGE = __MESSAGE + \";\"\r\n" +
                "TSDateString = [\"(*);*\"]\r\n" +
                "TSTimeString = [\"*;(*);*\"]\r\n" +
                "Timestamp = TSDateString + TSTimeString \r\n");

            int index = 1;
            StringBuilder regExpMiddle = new StringBuilder();

            foreach (DataDefinitionItem ddi in dataDefinitionItems)
            {
                iniContent.AppendLine(
                    "Value" + (index) + "Number = NumberFromHex([\"*;*;" + regExpMiddle.ToString() + "(*);*\"])\r\n" +
                    //                    "PRINT(" + "Value" + (index) + "Number" + ")\r\n" +
                    "Value" + (index) + "Number = 1.0*" + ddi.formel.Replace("x", "Value" + (index) + "Number") + "\r\n" +
                    //                    "PRINT(" + "Value" + (index) + "Number" + ")\r\n" +
                    "StoreEvent(\"" + dataCollector + "." + ddi.name + "\", \"" + ddi.name + "\", Timestamp, Value" + index + "Number)\r\n" +
                    "DynAttrCol = Add(\"" + dataCollector + "." + ddi.name + "\")\r\n");

                regExpMiddle.Append("*;");
                ++index;
            }

            iniContent.AppendLine("StoreElement(\"" + dataCollector + "\", \"My_Template\", DynAttrCol)"); // should be substituted by deviceID
        }

        private static void CreateINIFile()
        {
            using (StreamWriter writer = new StreamWriter(iniFilePath, false))
            {
                writer.Write(iniContent.ToString());
            }
        }

        class DataDefinitionItem
        {
            public string name = "";
            public string type = "";
            public string formel = "";
            // public string dimension;
            // public string text;

            public DataDefinitionItem(string name, string type, string formel)
            {
                this.name = name;
                this.type = type;
                this.formel = formel;
            }
        }
    }
}
