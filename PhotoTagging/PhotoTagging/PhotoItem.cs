using System.ComponentModel;
using System.Windows.Media;

namespace PhotoTagging
{
    public class PhotoItem : INotifyPropertyChanged
    {
        private string mName;
        private string mFileName;
        private string mExt;
        private long mSize;
        private int mTagging;

        public string Name
        {
            get { return mName; }
            set { mName = value; OnPropertyChanged("Name"); }
        }

        public string FileName
        {
            get { return mFileName; }
            set { mFileName = value; OnPropertyChanged("FileName"); }
        }

        public string Ext
        {
            get { return mExt; }
            set { mExt = value; OnPropertyChanged("Ext"); }
        }

        public long Size
        {
            get { return mSize; }
            set { mSize = value; OnPropertyChanged("Size"); }
        }

        public int Tagging
        {
            get { return mTagging; }
            set { mTagging = value; OnPropertyChanged("Tagging"); }
        }

        private string mPath;

        public string Path
        {
            get { return mPath; }
            set { mPath = value; OnPropertyChanged("Path"); }
        }

        private ImageSource mIcon;

        public ImageSource Icon
        {
            get { return mIcon; }
            set { mIcon = value; OnPropertyChanged("Icon"); }
        }

        private bool mIsChecked;

        public bool IsChecked
        {
            get { return mIsChecked; }
            set { mIsChecked = value; OnPropertyChanged("IsChecked"); }
        }

        public event PropertyChangedEventHandler PropertyChanged;

        private void OnPropertyChanged(string property)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(property));
        }
    }
}
