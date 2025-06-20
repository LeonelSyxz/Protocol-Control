# ui/tabs/hls.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QMessageBox
)
from PySide6.QtCore import Qt
from database import db
from controllers.hls import HLSController

class HLSTab(QWidget):
    def __init__(self):
        super().__init__()
        self.hls_controller = HLSController()
        self.loop_running = False

        self.setLayout(QVBoxLayout())

        self._create_interval_section()
        self._create_tv_table()
        self._create_control_buttons()

        self.load_data()

    def _create_interval_section(self):
        layout = QHBoxLayout()

        label = QLabel("Loop interval (seconds):")
        self.interval_spinbox = QSpinBox()
        self.interval_spinbox.setRange(1, 3600)
        self.interval_spinbox.setValue(db.get_loop_interval())
        self.interval_spinbox.valueChanged.connect(self.update_interval)

        layout.addWidget(label)
        layout.addWidget(self.interval_spinbox)
        layout.addStretch()

        self.layout().addLayout(layout)

    def _create_tv_table(self):
        self.tv_table = QTableWidget(0, 6)
        self.tv_table.setHorizontalHeaderLabels(["Name", "IP", "System", "Direction", "Status", "Actions"])
        self.tv_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout().addWidget(self.tv_table)

    def _create_control_buttons(self):
        layout = QHBoxLayout()

        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.add_row)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_changes)

        self.toggle_loop_btn = QPushButton("Start Loop")
        self.toggle_loop_btn.clicked.connect(self.toggle_loop)

        layout.addWidget(self.add_btn)
        layout.addWidget(self.save_btn)
        layout.addStretch()
        layout.addWidget(self.toggle_loop_btn)

        self.layout().addLayout(layout)

    def load_data(self):
        self.tv_table.setRowCount(0)
        for tv in db.get_tvs():
            self._add_tv_row(tv)

    def _add_tv_row(self, tv):
        row = self.tv_table.rowCount()
        self.tv_table.insertRow(row)

        name_item = QTableWidgetItem(tv[1])
        name_item.setData(Qt.ItemDataRole.UserRole, tv[0])

        ip_item = QTableWidgetItem(tv[2])

        os_combo = QComboBox()
        os_combo.addItems(["Google TV", "Roku OS"])
        if tv[3] in ["Google TV", "Roku OS"]:
            os_combo.setCurrentText(tv[3])
            
        direction_combo = QComboBox()
        direction_combo.addItems(["Up", "Down"])
        if len(tv) >= 6:
            direction_combo.setCurrentText(tv[4])

        status_combo = QComboBox()
        status_combo.addItems(["Active", "Inactive"])
        status_combo.setCurrentText("Active" if tv[5] else "Inactive")

        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(lambda _, ip=tv[2]: self.delete_row_by_ip(ip))

        self.tv_table.setItem(row, 0, name_item)
        self.tv_table.setItem(row, 1, ip_item)
        self.tv_table.setCellWidget(row, 2, os_combo)
        self.tv_table.setCellWidget(row, 3, direction_combo)
        self.tv_table.setCellWidget(row, 4, status_combo)
        self.tv_table.setCellWidget(row, 5, delete_btn)
        self.tv_table.setRowHeight(row, 32)

    def add_row(self):
        row = self.tv_table.rowCount()
        self.tv_table.insertRow(row)

        count = self.tv_table.rowCount()
        name_item = QTableWidgetItem(f"TV {count}")
        ip_item = QTableWidgetItem("192.168.0.0")

        os_combo = QComboBox()
        os_combo.addItems(["Google TV", "Roku OS"])
        
        direction_combo = QComboBox()
        direction_combo.addItems(["Up", "Down"])

        status_combo = QComboBox()
        status_combo.addItems(["Active", "Inactive"])

        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(lambda: self.tv_table.removeRow(row))

        self.tv_table.setItem(row, 0, name_item)
        self.tv_table.setItem(row, 1, ip_item)
        self.tv_table.setCellWidget(row, 2, os_combo)
        self.tv_table.setCellWidget(row, 3, direction_combo)
        self.tv_table.setCellWidget(row, 4, status_combo)
        self.tv_table.setCellWidget(row, 5, delete_btn)
        self.tv_table.setRowHeight(row, 32)

    def delete_row_by_ip(self, ip):
        tvs = db.get_tvs()
        for tv in tvs:
            if tv[2] == ip:
                db.delete_tv(tv[0])
                break
        self.load_data()

    def save_changes(self):
        seen_ips = set()

        for row in range(self.tv_table.rowCount()):
            ip_item = self.tv_table.item(row, 1)
            ip = ip_item.text()

            if ip in seen_ips:
                QMessageBox.warning(self, "Duplicate IP", f"The IP '{ip}' is duplicated.")
                return
            seen_ips.add(ip)

        for row in range(self.tv_table.rowCount()):
            name_item = self.tv_table.item(row, 0)
            ip_item = self.tv_table.item(row, 1)

            tv_id = name_item.data(Qt.ItemDataRole.UserRole)
            name = name_item.text()
            ip = ip_item.text()
            os = self.tv_table.cellWidget(row, 2).currentText()
            direction = self.tv_table.cellWidget(row, 3).currentText()
            status_str = self.tv_table.cellWidget(row, 4).currentText()
            status = 1 if status_str == "Active" else 0

            if tv_id is not None:
                db.update_tv(tv_id, name, ip, os, direction, status)
            else:
                db.add_tv(name, ip, os, direction, status)

        QMessageBox.information(self, "Saved", "Changes were saved successfully.")
        self.load_data()

    def update_interval(self, value):
        db.update_loop_interval(value)

    def toggle_loop(self):
        if not self.loop_running:
            self.hls_controller.start_loop()
            self.toggle_loop_btn.setText("Stop Loop")
        else:
            self.hls_controller.stop_loop()
            self.toggle_loop_btn.setText("Start Loop")
        self.loop_running = not self.loop_running
