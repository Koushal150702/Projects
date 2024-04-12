#include "mainwindow.h"
#include "functions.h"
#include <QApplication>

#define defaultThresholdSize 30 //setting the default size as 30M

int FileMonitorThread::thresholdSize = defaultThresholdSize;
QMutex FileMonitorThread::t;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    MainWindow w;
    w.show();

    return a.exec();
}
