import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QMessageBox, QPlainTextEdit, QLabel, QComboBox
from PyQt5.QtGui import QColor, QIcon, QPixmap

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Orkhan Todo List")
        
        self.tasks = self.load_tasks()

        layout = QVBoxLayout()
        self.setLayout(layout)

        name_layout = QHBoxLayout()  # Layout for Name field
        layout.addLayout(name_layout)

        name_label = QLabel("Name:")  # Label for Name field
        name_layout.addWidget(name_label)

        self.name_entry = QLineEdit()  # Add QLineEdit for name
        name_layout.addWidget(self.name_entry)  # Add QLineEdit to layout

        task_name_layout = QHBoxLayout()  # Layout for Task Name field
        layout.addLayout(task_name_layout)

        task_name_label = QLabel("Task Name:")  # Label for Task Name field
        task_name_layout.addWidget(task_name_label)

        self.task_entry = QLineEdit()  # Add QLineEdit for task
        task_name_layout.addWidget(self.task_entry)  # Add QLineEdit to layout

        priority_layout = QHBoxLayout()  # Layout for Priority field
        layout.addLayout(priority_layout)

        priority_label = QLabel("Priority:")  # Label for Priority field
        priority_layout.addWidget(priority_label)

        self.priority_combo = QComboBox()  # Add QComboBox for priority
        self.priority_combo.addItem(self.create_color_icon(QColor("red")), "High")  # Add colored square icons alongside priority levels
        self.priority_combo.addItem(self.create_color_icon(QColor("green")), "Medium")
        self.priority_combo.addItem(self.create_color_icon(QColor("blue")), "Low")
        priority_layout.addWidget(self.priority_combo)  # Add QComboBox to layout

        description_layout = QHBoxLayout()  # Layout for Description field
        layout.addLayout(description_layout)

        description_label = QLabel("Description:")  # Label for Description field
        description_layout.addWidget(description_label)

        self.description_entry = QPlainTextEdit()  # Multiline text field for description
        description_layout.addWidget(self.description_entry)  # Add multiline text field to layout

        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task)
        layout.addWidget(add_button)

        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        mark_completed_button = QPushButton("Mark as Completed")
        mark_completed_button.clicked.connect(self.complete_task)
        layout.addWidget(mark_completed_button)

        undo_completed_button = QPushButton("Undo Completed Task")
        undo_completed_button.clicked.connect(self.undo_completed_task)
        layout.addWidget(undo_completed_button)

        delete_button = QPushButton("Delete Task")
        delete_button.clicked.connect(self.delete_task)
        layout.addWidget(delete_button)

        self.view_tasks()

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                tasks = json.load(file)
        except FileNotFoundError:
            tasks = []
        return tasks

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file)

    def add_task(self):
        name = self.name_entry.text()  # Retrieve name
        task = self.task_entry.text()
        priority = self.priority_combo.currentText()  # Retrieve priority
        description = self.description_entry.toPlainText()  # Retrieve description text from QPlainTextEdit
        if task:
            self.tasks.append({'name': name, 'task': task, 'priority': priority, 'description': description, 'completed': False})  # Include name and priority
            self.save_tasks()
            self.name_entry.clear()  # Clear name entry
            self.task_entry.clear()
            self.description_entry.clear()  # Clear description entry
            self.view_tasks()
        else:
            QMessageBox.warning(self, "Warning", "Task cannot be empty!")

    def view_tasks(self):
        self.task_list.clear()
        for task in self.tasks:
            completed_indicator = 'x' if task['completed'] else ' '
            priority = task.get('priority', '')  # Get priority or empty string if not found
            task_display = f"[{completed_indicator}] {task['task']}"
            if priority:  # Only include priority if available
                task_display += f" - Priority: {priority}"
            description = task.get('description', '')  # Get description or empty string if not found
            if description:  # Only include description if available
                task_display += f"\nDescription: {description}"
            if 'name' in task:  # Check if name exists
                task_display = f"{task['name']}: {task_display}"  # Add name to task display
            self.task_list.addItem(task_display)

    def complete_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            task_index = self.task_list.row(selected_item)
            self.tasks[task_index]['completed'] = True
            self.save_tasks()
            self.view_tasks()
        else:
            QMessageBox.warning(self, "Warning", "Please select a task to mark as completed.")

    def undo_completed_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            task_index = self.task_list.row(selected_item)
            self.tasks[task_index]['completed'] = False
            self.save_tasks()
            self.view_tasks()
        else:
            QMessageBox.warning(self, "Warning", "Please select a completed task to mark as incomplete.")

    def delete_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            task_index = self.task_list.row(selected_item)
            del self.tasks[task_index]
            self.save_tasks()
            self.view_tasks()
        else:
            QMessageBox.warning(self, "Warning", "Please select a task to delete.")

    def create_color_icon(self, color):
        pixmap = QPixmap(10, 10)
        pixmap.fill(color)
        icon = QIcon(pixmap)
        return icon

def main():
    app = QApplication([])
    todo_app = TodoApp()
    todo_app.show()
    app.exec_()

if __name__ == "__main__":
    main()
