#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QStringListModel>
#include <QDir>
#include <QProcess>
#include <QTextBrowser>
#include <QFrame>
#include <QProcess>
#include <QTextBrowser>
#include <QFrame>
#include <QMessageBox>
#include <QInputDialog>
#include "functions.h"

using namespace std;

namespace Ui {
class MainWindow;
}

map<string, char> return_files_with_type(string curr_path);

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    void ShowContextMenu(const QPoint& pos);
    void CompressFile();
    void DeleteFile(string file, bool isFile);
    void ViewFileProperties(string file);
    void RefreshFileList();
    ~MainWindow();

private slots:
    void on_tableWidget_cellClicked(int row);
    void on_btnOpen_clicked();
    void on_btnBack_clicked();
    void on_btnFront_clicked();
    void on_btnDelete_clicked();
    void on_btnCompress_clicked();
    void on_actionThresholdSize_triggered();
    void on_btnSearch_clicked();
    void on_btnHome_clicked();
    void on_btnBackCheck_clicked();

    void on_actionFunctions_triggered();

private:
    Ui::MainWindow *ui;
    map<string, char> map_of_files;
    string clicked_file;
    string homePath;
    string currentPath;
    list<string> previousPath;
    list<string> nextPath;
    FileMonitorThread *fileMonitorThread;
    void createInstanceOfFileMonitorThread();
    void Compress(string File, bool isFile);
    void Compress_F(string File, bool isFile);
};

#endif
