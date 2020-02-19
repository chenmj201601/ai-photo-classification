using System.Collections.Generic;
using System.Xml.Serialization;

namespace PhotoTagging
{
    [XmlRoot("Taggings")]
    public class PhotoTaggings
    {
        private List<Photo> mListPhotos = new List<Photo>();

        [XmlArray("Photos")]
        [XmlArrayItem("Photo")]
        public List<Photo> Photos
        {
            get { return mListPhotos; }
        }
    }
}
