using NetInfo.Common;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Imaging;

namespace PhotoTagging
{
    /// <summary>
    /// MainWindow.xaml 的交互逻辑
    /// </summary>
    public partial class MainWindow : Window
    {
        private bool mIsInited;

        private List<Photo> mListPhotos = new List<Photo>();
        private ObservableCollection<PhotoItem> mListPhotoItems = new ObservableCollection<PhotoItem>();
        private string mPhotoDir = "D:\\temp\\photo-classification\\photos";
        private string mTaggingDir = "D:\\temp\\photo-classification";
        private string mTaggingName = "tagging.xml";
        private int mTotalCount = 0;
        private int mPageSize = 200;
        private int mPageCount = 0;
        private int mPageIndex = 0;

        public MainWindow()
        {
            InitializeComponent();

            Loaded += MainWindow_Loaded;
            BtnTag.Click += BtnTag_Clicked;
            BtnGen.Click += BtnGen_Clicked;
            BtnGenTrain.Click += BtnGenTrain_Clicked;
            BtnGenValid.Click += BtnGenValid_Clicked;
            BtnGenTest.Click += BtnGenTest_Clicked;
            BtnFirst.Click += BtnFirst_Clicked;
            BtnPre.Click += BtnPre_Clicked;
            BtnNext.Click += BtnNext_Clicked;
            BtnLast.Click += BtnLast_Clicked;
            BtnSkip.Click += BtnSkip_Clicked;
        }

        private void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            WindowState = WindowState.Maximized;
            if (!mIsInited)
            {
                Init();
                mIsInited = true;
            }
        }

        private void Init()
        {
            ListBoxPhotos.ItemsSource = mListPhotoItems;
            ShowPageTip();
            BackgroundWorker worker = new BackgroundWorker();
            worker.DoWork += (s, de) =>
            {
                LoadPhotos();
            };
            worker.RunWorkerCompleted += (s, re) =>
            {
                worker.Dispose();

                InitPhotoItem();
            };
            worker.RunWorkerAsync();
        }

        private void LoadPhotos()
        {
            mListPhotos.Clear();
            try
            {
                DirectoryInfo dirInfo = new DirectoryInfo(mPhotoDir);
                FileInfo[] fileInfos = dirInfo.GetFiles();
                for (int i = fileInfos.Length - 1; i >= 0; i--)
                {
                    FileInfo fileInfo = fileInfos[i];
                    string name = fileInfo.Name;
                    Photo info = new Photo();
                    info.Name = name;
                    info.FileName = name;
                    info.Ext = fileInfo.Extension;
                    info.Size = fileInfo.Length;
                    mListPhotos.Add(info);
                }
                int totalCount = fileInfos.Length;
                mTotalCount = totalCount;
                int pageSize = mPageSize;
                int pageCount = totalCount / pageSize;
                if ((totalCount % pageSize) != 0)
                {
                    pageCount++;
                }
                mPageCount = pageCount;
                mPageIndex = 0;
                ShowPageTip();
            }
            catch (Exception ex)
            {
                ShowException(ex.Message);
            }
        }

        private void InitPhotoItem()
        {
            mListPhotoItems.Clear();
            try
            {
                for (int i = mPageIndex * mPageSize; i < (mPageIndex + 1) * mPageSize && i < mListPhotos.Count; i++)
                {
                    Photo photo = mListPhotos[i];
                    PhotoItem item = new PhotoItem();
                    item.Name = photo.Name;
                    item.FileName = photo.FileName;
                    item.Icon = GetThumbIcon(item);
                    item.Path = Path.Combine(mPhotoDir, photo.FileName);
                    item.FileName = photo.FileName;
                    item.Ext = photo.Ext;
                    item.Size = photo.Size;
                    mListPhotoItems.Add(item);
                }
            }
            catch (Exception ex)
            {
                ShowException(ex.Message);
            }
        }

        private void TaggingPhoto()
        {
            try
            {
                OperationReturn optReturn;
                string taggingDir = mTaggingDir;
                string taggingName = mTaggingName;
                if (!Directory.Exists(taggingDir))
                {
                    Directory.CreateDirectory(taggingDir);
                }
                string taggingPath = Path.Combine(taggingDir, taggingName);
                PhotoTaggings taggings = null;
                if (File.Exists(taggingPath))
                {
                    optReturn = XMLHelper.DeserializeFile<PhotoTaggings>(taggingPath);
                    if (!optReturn.Result)
                    {
                        ShowException(string.Format("Fail.\t{0}\t{1}", optReturn.Code, optReturn.Message));
                        return;
                    }
                    taggings = optReturn.Data as PhotoTaggings;
                }
                if (taggings == null)
                {
                    taggings = new PhotoTaggings();
                }
                List<PhotoItem> selectedPhotoItems = new List<PhotoItem>();
                var listItems = ListBoxPhotos.SelectedItems;
                foreach (var item in listItems)
                {
                    var photoItem = item as PhotoItem;
                    if (photoItem != null)
                    {
                        selectedPhotoItems.Add(photoItem);
                    }
                }
                foreach (var item in selectedPhotoItems)
                {
                    string name = item.Name;
                    var photo = taggings.Photos.FirstOrDefault(p => p.Name.Equals(name));
                    if (photo == null)
                    {
                        photo = new Photo();
                        photo.Name = name;
                        photo.FileName = item.FileName;
                        photo.Ext = item.Ext;
                        photo.Size = item.Size;
                        taggings.Photos.Add(photo);
                    }
                    photo.Tagging = (int)TaggingType.Me;
                }
                var sortedPhotos = taggings.Photos.OrderBy(p => p.Name).ToList(); ;
                taggings.Photos.Clear();
                foreach (var photo in sortedPhotos)
                {
                    taggings.Photos.Add(photo);
                }
                optReturn = XMLHelper.SerializeFile(taggings, taggingPath);
                if (!optReturn.Result)
                {
                    ShowException(string.Format("Fail.\t{0}\t{1}", optReturn.Code, optReturn.Message));
                    return;
                }
                ShowInformation(string.Format("Tagging end!"));
            }
            catch (Exception ex)
            {
                ShowException(ex.Message);
            }
        }

        private ImageSource GetThumbIcon(PhotoItem photoItem)
        {
            string path = Path.Combine(mPhotoDir, photoItem.FileName);
            BitmapImage img = new BitmapImage();
            img.BeginInit();
            img.CacheOption = BitmapCacheOption.None;
            img.UriSource = new Uri(path);
            img.DecodePixelHeight = 90;
            img.EndInit();
            return img;
        }

        private void ShowPageTip()
        {
            Dispatcher.Invoke(new Action(() =>
            {
                try
                {
                    TxtPage.Text = string.Format("第 {0} 页 / 共 {1} 页 每页 {2} 幅，共 {3} 幅", mPageIndex + 1, mPageCount, mPageSize, mTotalCount);
                    TxtSkip.Text = string.Format("{0}", mPageIndex + 1);
                }
                catch (Exception ex)
                {
                    ShowException(ex.Message);
                }
            }));
        }

        private void BtnTag_Clicked(object sender, RoutedEventArgs e)
        {
            TaggingPhoto();
        }

        private void BtnGen_Clicked(object sender,RoutedEventArgs e)
        {

        }

        private void BtnGenTrain_Clicked(object sender, RoutedEventArgs e)
        {
           
        }

        private void BtnGenValid_Clicked(object sender, RoutedEventArgs e)
        {

        }

        private void BtnGenTest_Clicked(object sender, RoutedEventArgs e)
        {

        }

        private void BtnFirst_Clicked(object sender, RoutedEventArgs e)
        {
            mPageIndex = 0;
            InitPhotoItem();
            ShowPageTip();
        }

        private void BtnPre_Clicked(object sender, RoutedEventArgs e)
        {
            if (mPageIndex > 0)
            {
                mPageIndex--;
                InitPhotoItem();
                ShowPageTip();
            }
        }

        private void BtnNext_Clicked(object sender, RoutedEventArgs e)
        {
            if (mPageIndex < mPageCount - 1)
            {
                mPageIndex++;
                InitPhotoItem();
                ShowPageTip();
            }
        }

        private void BtnLast_Clicked(object sender, RoutedEventArgs e)
        {
            mPageIndex = mPageCount - 1;
            InitPhotoItem();
            ShowPageTip();
        }

        private void BtnSkip_Clicked(object sender, RoutedEventArgs e)
        {
            string strPage = TxtSkip.Text;
            int pageIndex;
            if (int.TryParse(strPage, out pageIndex))
            {
                if (pageIndex > 0)
                {
                    mPageIndex = pageIndex - 1;
                    InitPhotoItem();
                    ShowPageTip();
                }
            }
        }

        private void ShowException(string msg)
        {
            MessageBox.Show(msg, "PhotoTagging", MessageBoxButton.OK, MessageBoxImage.Error);
        }

        private void ShowInformation(string msg)
        {
            MessageBox.Show(msg, "PhotoTagging", MessageBoxButton.OK, MessageBoxImage.Information);
        }
    }
}
