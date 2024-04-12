#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include <QThread>
#include <iostream>
#include <map>
#include <fstream>
#include <sstream>
#include <vector>
#include <QMutex>
#include <QMutexLocker>
using namespace std;

map<string, char> return_files_with_type(string curr_path);
int return_count_of_files_in_dir(string curr_path);

class FileMonitorThread : public QThread {
private:
    static int thresholdSize;
    string homePath;
    static QMutex t;
    vector<string> largeFiles;
    bool askUserforAction;

protected:
    void run() override;

public:
    FileMonitorThread(QObject *parent = nullptr) :  QThread(parent), homePath("/home/cse/"), askUserforAction(false) {}
    string getHomePath() { return homePath; }
    static int getThresholdSize() { return thresholdSize; }
    static void setThresholdSize(int s) { thresholdSize = s; }
    vector<string> getLargeFiles() const;
};

#endif
