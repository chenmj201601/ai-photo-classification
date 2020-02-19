using System.Xml.Serialization;

namespace PhotoTagging
{
    [XmlRoot("Photo")]
    public class Photo
    {
        [XmlElement("Name")]
        public string Name { get; set; }
        [XmlElement("File")] 
        public string FileName { get; set; }
        [XmlElement("Ext")] 
        public string Ext { get; set; }
        [XmlElement("Size")] 
        public long Size { get; set; }
        [XmlElement("Tagging")] 
        public int Tagging { get; set; }
    }
}
