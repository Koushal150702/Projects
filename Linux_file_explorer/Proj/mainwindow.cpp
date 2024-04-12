#include "mainwindow.h"
#include "ui_mainwindow.h"

void MainWindow::RefreshFileList() {
    ui->tableWidget->clearContents();
    int numFiles = map_of_files.size();
    ui->tableWidget->setRowCount(numFiles);
    int r = 0;
    for (const auto& pair : map_of_files) {
        QString fileName = QString::fromStdString(pair.first);
        QString fileType = QString(pair.second == 'd' ? "Directory" : "File");

        ui->tableWidget->setItem(r, 0, new QTableWidgetItem(fileName));
        ui->tableWidget->setItem(r, 1, new QTableWidgetItem(fileType));
        ++r;
    }
    ui->lblCurrentPath->setText(QString::fromStdString(currentPath));
    ui->btnOpen->setEnabled(false);
    ui->btnDelete->setEnabled(false);
    ui->btnCompress->setEnabled(false);
}

void MainWindow::createInstanceOfFileMonitorThread() {
    this->fileMonitorThread = new FileMonitorThread(this);
}

MainWindow::MainWindow(QWidget *parent) :  QMainWindow(parent), ui(new Ui::MainWindow) {
    ui->setupUi(this);
    ui->tableWidget->setEditTriggers(QAbstractItemView::NoEditTriggers);
    ui->btnOpen->setEnabled(false);
    ui->btnDelete->setEnabled(false);
    ui->btnCompress->setEnabled(false);
    ui->btnBack->setEnabled(false);
    ui->btnFront->setEnabled(false);

    createInstanceOfFileMonitorThread();

    this->currentPath = this->fileMonitorThread->getHomePath();
    this->homePath = this->currentPath;
    this->map_of_files = return_files_with_type(currentPath);

    ui->tableWidget->setColumnCount(2);

    RefreshFileList();

    ui->tableWidget->resizeColumnsToContents();
    ui->tableWidget->resize(400,600);
    ui->tableWidget->setHorizontalHeaderLabels({"File Name", "Type"});
}

MainWindow::~MainWindow() {
    delete ui;
}
string path_file(const string& clicked_file) {
    string file = clicked_file;
    int pos = 0;
    while ((pos = file.find(' ', pos)) != string::npos) {
            file.replace(pos, 1, "\\ ");
            pos += 2;
    }
    return file;
}

void MainWindow::on_tableWidget_cellClicked(int row) {
    QString file = ui->tableWidget->item(row, 0)->text();
    clicked_file  = file.toStdString();
    bool enable_btnOpen = map_of_files[clicked_file] == 'd';
    ui->btnOpen->setEnabled(enable_btnOpen);    // btnOpen is to traverse through directories
    ui->btnCompress->setEnabled(true);
    ui->btnDelete->setEnabled(true);
    ViewFileProperties(clicked_file);
}

void MainWindow::ViewFileProperties(string file) {
  QString path = QString::fromStdString(path_file(currentPath)) + QString::fromStdString(file);
  QFileInfo fileInfo(path);
  path = QString::fromStdString(path_file(path.toStdString()));
  if (fileInfo.exists()) {
    // to print the type, location, permissions, size
    QFile::Permissions permissions = fileInfo.permissions();
    ui -> fileProperties -> setText("");

    string nfile = "stat -c %F " + path.toStdString();
    FILE *filename = popen(nfile.c_str(), "r");

    if (!filename) {
      QMessageBox::critical(this, "Error", "Failed to find the file name.");
      return;
    }

    // Read the output of the command
    char buffer[128];
    std::string result = "";
    while (fgets(buffer, sizeof(buffer), filename) != nullptr) {
      result += buffer;
    }

    // Display or process the result as needed
    ui -> fileProperties -> append("File type: " + QString::fromStdString(result));
    pclose(filename);

    ui -> fileProperties -> append("Location: " + path + "\n\nPermissions:");

    QString y, g, o;
    QString r = permissions & QFile::ReadOwner ? "Can read" : "Cannot read";
    y = "Owners: " + r;
    r = permissions & QFile::WriteOwner ? "can write" : "cannot write";
    y += ", " + r;
    r = permissions & QFile::ExeOwner ? "can execute" : "cannot execute";
    y += ", " + r;
    ui -> fileProperties -> append(y);

    QString gr = permissions & QFile::ReadGroup ? "Can read" : "Cannot read";
    g = "Group: " + gr;
    gr = permissions & QFile::WriteGroup ? "can write" : "cannot write";
    g += ", " + gr;
    gr = permissions & QFile::ExeGroup ? "can execute" : "cannot execute";
    g += ", " + gr;
    ui -> fileProperties -> append(g);

    QString v = permissions & QFile::ReadOther ? "Can read" : "Cannot read";
    o = "Others: " + v;
    v = permissions & QFile::WriteOther ? "can write" : "cannot write";
    o += ", " + v;
    v = permissions & QFile::ExeOther ? "can execute" : "cannot execute";
    o += ", " + v;
    ui -> fileProperties -> append(o);

    string size = "stat -c %s " + path.toStdString();

    FILE * s = popen(size.c_str(), "r");
    if (!s) {
      QMessageBox::critical(this, "Error", "Failed to find the file size.");
      return;
    }
    char buff[128];
    std::string res = "";
    while (fgets(buff, sizeof(buff), s) != nullptr) {
      res += buff;
    }

    ui -> fileProperties -> append("\nSize of file: " + QString::fromStdString(res));
    pclose(s);

    string tsize = "du -bs | cut -f1";
    FILE * ts = popen(tsize.c_str(), "r");
    if (!ts) {
      QMessageBox::critical(this, "Error", "Failed to find the total size.");
      return;
    }
    char buf[128];
    std::string total = "";
    while (fgets(buf, sizeof(buf), ts) != nullptr) {
      total += buf;
    }

    ui -> fileProperties -> append("\nTotal disk usage: " + QString::fromStdString(total));
    pclose(ts);

    ui -> progressBar -> setMinimum(0);
    ui -> progressBar -> setMaximum(std::stoi(total));
    ui -> progressBar -> setValue(std::stoi(res));
  }
}

void MainWindow::on_btnOpen_clicked() {
    previousPath.push_back(currentPath);

    string file = path_file(clicked_file);

    currentPath += file + "/";
    nextPath.clear();

    map_of_files = return_files_with_type(currentPath);
    RefreshFileList();

    ui->btnBack->setEnabled(true);
    ui->btnFront->setEnabled(false);
}

void MainWindow::on_btnBack_clicked() {
    if (previousPath.empty())
        ui->btnBack->setEnabled(false);

    nextPath.push_back(currentPath);
    currentPath = previousPath.back();
    previousPath.pop_back();

    map_of_files = return_files_with_type(currentPath);
    RefreshFileList();

    ui->btnBack->setEnabled(!previousPath.empty());
    ui->btnFront->setEnabled(true);
}

void MainWindow::on_btnFront_clicked()
{
    if (nextPath.empty())
        ui->btnFront->setEnabled(false);

    previousPath.push_back(currentPath);
    currentPath = nextPath.back();
    nextPath.pop_back();

    map_of_files = return_files_with_type(currentPath);
    RefreshFileList();

    ui->btnBack->setEnabled(true);
    ui->btnFront->setEnabled(!nextPath.empty());
}

void MainWindow::on_btnDelete_clicked()
{
    string confirmationMessage =  "Are you sure you want to delete: " + clicked_file;
    QMessageBox::StandardButton reply = QMessageBox::question(this, "Confirmation", confirmationMessage.c_str(), QMessageBox::Yes | QMessageBox::No);

    if (reply ==  QMessageBox::No)
        return;

    string file = path_file(clicked_file);
    string deleteClickedFile = "rm -r " + currentPath + file;
    FILE *abs_path_to_files = popen(deleteClickedFile.c_str(), "r");

    if (!abs_path_to_files) {
        QMessageBox::critical(this, "Error", "Failed to delete the file.");
        return ;
    }
    QMessageBox::information(this, "Information", "File deleted successfully.");

    if (currentPath+clicked_file + "/" == nextPath.back())
        nextPath.clear();

    map_of_files = return_files_with_type(currentPath);
    RefreshFileList();
    if (nextPath.empty())
        ui->btnFront->setEnabled(false);
}

void MainWindow::on_actionThresholdSize_triggered() {
    bool isChanged;
    QString currentThresholdSize = QString::number(FileMonitorThread::getThresholdSize());
    QString newSize = QInputDialog::getText(this, tr("Set Threshold Size"), tr("Enter the new threshold size:"), QLineEdit::Normal, currentThresholdSize, &isChanged);
    if (isChanged && !newSize.isEmpty()) {
        int newSizeInt = newSize.toInt(&isChanged);
        if (isChanged)
            FileMonitorThread::setThresholdSize(newSizeInt);
        else
            QMessageBox::critical(this, "Error", "Enter an Integer value for the Threshold Size!");
    }
    else if (isChanged && newSize.isEmpty()) {
        QMessageBox::critical(this, "Error", "Threshold Size cannot be Empty!");
    }
}

void MainWindow::Compress(string File, bool isFile){
    string ziparg;
    if (isFile) {
        QString compressedFileName = QInputDialog::getText(this, "Enter Compressed File Name", "Enter the name for the compressed file:");
        ziparg = "zip " + currentPath + compressedFileName.toStdString() + ".zip " + currentPath + File;
    } else {
        QString compressedFileName = QInputDialog::getText(this, "Enter Compressed Directory Name", "Enter the name for the compressed directory:");
        ziparg = "zip " + currentPath + compressedFileName.toStdString() + ".zip " + currentPath + File;
    }
    FILE *abs_path_to_files = popen(ziparg.c_str(), "r");
    if (!abs_path_to_files) {
        QMessageBox::critical(this, "Error", "Failed to delete the file.");
        return ;
    }
}

void MainWindow::on_btnCompress_clicked() {
    string File = path_file(clicked_file);
    bool isFile = map_of_files[File] == 'f';
    Compress(File, isFile);
    RefreshFileList();
}

void MainWindow::on_btnSearch_clicked() {
    string file_to_search = (ui->searchText->text()).toStdString();
    string pathfile_to_search = path_file(file_to_search);

    string arg_files = "find " + homePath + " -name " + pathfile_to_search;
    FILE *path_to_files = popen(arg_files.c_str(), "r");
    if (!path_to_files) {
        cerr << "Error finding files!" << endl;
        return ;
    }

    char buffer_reader[128];
    ostringstream ostream;
    while (fgets(buffer_reader, sizeof(buffer_reader), path_to_files) != nullptr) {
        ostream << buffer_reader;
    }

    istringstream lines_of_all_files(ostream.str());
    string path_to_file;
    getline(lines_of_all_files, path_to_file);

    if (path_to_file.empty()){
        QMessageBox::critical(this, "Error", "File was not found!");
    }
    else {
        path_to_file = path_file(path_to_file);
        int pos = path_to_file.find(pathfile_to_search);
        path_to_file = path_to_file.substr(0, pos);
        currentPath = path_to_file;

        map_of_files = return_files_with_type(currentPath);
        nextPath.clear();
        previousPath.clear();
        ui->btnBack->setEnabled(false);
        ui->btnFront->setEnabled(false);
        RefreshFileList();
    }
    ui->searchText->clear();
}

void MainWindow::on_btnHome_clicked() {
    this->map_of_files = return_files_with_type(homePath);
    currentPath = homePath;
    nextPath.clear();
    previousPath.clear();
    ui->btnBack->setEnabled(false);
    ui->btnFront->setEnabled(false);
    RefreshFileList();
}

void MainWindow::DeleteFile(string File, bool isFile) {
    string confirmationMessage =  "Are you sure you want to delete: " + File;
    QMessageBox::StandardButton reply = QMessageBox::question(this, "Confirmation", confirmationMessage.c_str(), QMessageBox::Yes | QMessageBox::No);

    if (reply ==  QMessageBox::No)
        return;

    string rmarg;
    if (isFile) {
        rmarg = "rm -f " + File;
    } else {
        rmarg = "rm -rf " + File;
    }
    FILE *abs_path_to_files = popen(rmarg.c_str(), "r");
    if (!abs_path_to_files) {
        QMessageBox::critical(this, "Error", "Failed to delete the file.");
        return ;
    }
    QMessageBox::information(this, "Information", "File deleted successfully.");
}

void MainWindow::on_btnBackCheck_clicked() {
    this->fileMonitorThread->start();
    this->fileMonitorThread->wait();

    QStringList qLargeFiles;
    for (int i = 0; i < this->fileMonitorThread->getLargeFiles().size(); i++){
        qLargeFiles.append(QString::fromStdString(this->fileMonitorThread->getLargeFiles().at(i)));
    }

    QString fileNamesText = "Following files are >"  +  QString::number(this->fileMonitorThread->getThresholdSize()) + "M:\n" + qLargeFiles.join("\n\n") + "\n\nPlease select an option:";

    QMessageBox msgBox;
    msgBox.setText(fileNamesText);

    QPushButton *deleteButton = msgBox.addButton("Delete All", QMessageBox::ActionRole);
    QPushButton *ignoreButton = msgBox.addButton("Ignore", QMessageBox::ActionRole);
    msgBox.setDefaultButton(ignoreButton);

    int userChoice = msgBox.exec();

   if (msgBox.clickedButton() == deleteButton) {
        for (int i = 0; i < qLargeFiles.size(); i++) {
            bool isFile = map_of_files[qLargeFiles.at(i).toStdString()] == 'f';
            DeleteFile(qLargeFiles.at(i).toStdString(), isFile);
        }
    } else {

    }
    createInstanceOfFileMonitorThread();
}


void MainWindow::on_actionFunctions_triggered() {
    QString text = "Options: Set threshold size as per choice.\n\n"
                  "Help: Displays all the functionalities of the features implemented in the application.\n\n"
                  "Home: Displays all the content from the home directory.\n\n"
                  "Background Check: Runs a background check which displays all the large files and asks the user if they want to delete all.\n\n"
                  "Search: Displays the content which the user wants to search for.\n\n"
                  "Progress Bar: Displays the size of file compared to the total disk usage.\n\n"
                  "Path: Displays the current location of the file as the file path.\n\n\n"
                  "The files when clicked on display the file properties such as the file type, location, file permissions and the size of file. It also displays the total disk usage of the current directory.\n\n"
                  "Files when clicked on can be opened if its a directory, can be compressed or deleted upon clicking the respective buttons.";


    QDialog* textDialog = new QDialog(this);
    textDialog->setWindowTitle("Documentation");

    QVBoxLayout* layout = new QVBoxLayout(textDialog);
    QTextEdit* textEdit = new QTextEdit(textDialog);
    textEdit->setReadOnly(true);
    textEdit->setPlainText(text);
    layout->addWidget(textEdit);
    textDialog->setLayout(layout);
    textDialog->resize(400, 300);

    textDialog->exec();
}

