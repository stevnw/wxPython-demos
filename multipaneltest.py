"""
This was created using Claude - purely as I wanted to see if a GUI like this could be done before I sunk time into it. As such, the actual logic is kind of busted and I cannot be fucked to fix it currently.
Generally though it might make a good base if I wanted to fix it. 

General problems are:
- "Last Completed" gets autofilled on tasks which havent been done yet in the GUI - on the CSV the tasks are stored in however this is not the case. 
- Doesnt seem to auto complete
- Repeating tasks seem to auto delete themselves randomly some times - honestly no fucking clue lol

"""
import wx
import csv
import os
from datetime import datetime, timedelta

class TodoTimerApp(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Todo Timer App')
        
        # File to store tasks
        self.tasks_file = 'todo_tasks.csv'
        
        # Ensure CSV exists with headers if it doesn't
        self.ensure_csv_exists()
        
        # Main panel
        panel = wx.Panel(self)
        
        # Main horizontal sizer
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Left side - Task List
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Task List
        self.task_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.task_list.InsertColumn(0, 'Task #', width=60)
        self.task_list.InsertColumn(1, 'Task Name', width=150)
        self.task_list.InsertColumn(2, 'Repeating', width=80)
        self.task_list.InsertColumn(3, 'Time', width=80)
        self.task_list.InsertColumn(4, 'Last Completed', width=120)
        
        # Load existing tasks
        self.load_tasks()
        
        left_sizer.Add(self.task_list, 1, wx.EXPAND | wx.ALL, 10)
        
        # Task Entry Section
        task_entry_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Task Name Input
        self.task_input = wx.TextCtrl(panel)
        task_entry_sizer.Add(self.task_input, 1, wx.ALL | wx.EXPAND, 5)
        
        # Time Input
        self.time_input = wx.SpinCtrl(panel, min=1, max=120, initial=25)
        task_entry_sizer.Add(self.time_input, 0, wx.ALL, 5)
        
        # Repeating Checkbox
        self.repeating_check = wx.CheckBox(panel, label="Repeating")
        task_entry_sizer.Add(self.repeating_check, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        left_sizer.Add(task_entry_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Add Task Button
        add_task_btn = wx.Button(panel, label='Add Task')
        add_task_btn.Bind(wx.EVT_BUTTON, self.on_add_task)
        left_sizer.Add(add_task_btn, 0, wx.EXPAND | wx.ALL, 10)
        
        # Right side - Timer
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Timer Display
        self.timer_display = wx.StaticText(panel, label='25:00', style=wx.ALIGN_CENTER)
        self.timer_display.SetFont(wx.Font(48, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        right_sizer.Add(self.timer_display, 0, wx.ALIGN_CENTER | wx.ALL, 20)
        
        # Start Timer Button
        start_timer_btn = wx.Button(panel, label='Start Timer')
        start_timer_btn.Bind(wx.EVT_BUTTON, self.start_timer)
        right_sizer.Add(start_timer_btn, 0, wx.EXPAND | wx.ALL, 10)
        
        # Add Left and Right Sizers to Main Sizer
        main_sizer.Add(left_sizer, 1, wx.EXPAND)
        main_sizer.Add(right_sizer, 1, wx.EXPAND)
        
        # Set Layout
        panel.SetSizer(main_sizer)
        
        # Timer setup
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_timer, self.timer)
        self.remaining_time = 25 * 60  # Default 25 minutes
        self.current_task_index = None
        
        self.SetSize((800, 600))
        self.Centre()
    
    def ensure_csv_exists(self):
        if not os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['TaskNumber', 'Task', 'Repeating', 'Time', 'Date', 'LastCompleted'])
    
    def load_tasks(self):
        # Clear existing items
        self.task_list.DeleteAllItems()
        
        with open(self.tasks_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row:  # Ensure row is not empty
                    self.task_list.Append(row[:5])
    
    def on_add_task(self, event):
        task = self.task_input.GetValue()
        time = self.time_input.GetValue()
        repeating = 'Yes' if self.repeating_check.GetValue() else 'No'
        
        # Determine task number by counting existing tasks
        task_number = self.task_list.GetItemCount() + 1
        
        # Append to list control
        self.task_list.Append([str(task_number), task, repeating, str(time), ''])
        
        # Save to CSV
        with open(self.tasks_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([task_number, task, repeating, time, datetime.now().strftime('%Y-%m-%d'), ''])
        
        # Clear inputs
        self.task_input.Clear()
        self.time_input.SetValue(25)
        self.repeating_check.SetValue(False)
    
    def start_timer(self, event):
        # Get selected task's time
        selected_item = self.task_list.GetFirstSelected()
        if selected_item == -1:
            wx.MessageBox('Please select a task', 'Error', wx.OK | wx.ICON_ERROR)
            return
        
        # Store selected task for completion tracking
        self.current_task_index = selected_item
        
        time_str = self.task_list.GetItemText(selected_item, 3)
        self.remaining_time = int(time_str) * 60
        
        # Start timer
        self.timer.Start(1000)  # 1 second interval
    
    def update_timer(self, event):
        if self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            timer_string = f'{mins:02d}:{secs:02d}'
            self.timer_display.SetLabel(timer_string)
            self.remaining_time -= 1
        else:
            self.timer.Stop()
            self.timer_display.SetLabel('00:00')
            
            # Automatically complete the current task
            self.complete_current_task()
            
            wx.MessageBox('Timer Completed!', 'Done', wx.OK | wx.ICON_INFORMATION)
    
    def complete_current_task(self):
        # Get task details
        task_number = self.task_list.GetItemText(self.current_task_index, 0)
        task = self.task_list.GetItemText(self.current_task_index, 1)
        repeating = self.task_list.GetItemText(self.current_task_index, 2)
        
        # Read entire CSV
        with open(self.tasks_file, 'r') as file:
            reader = list(csv.reader(file))
        
        # Write back to CSV with only the specific task updated
        with open(self.tasks_file, 'w', newline='') as file:
            writer = csv.writer(file)
            
            # Write headers first
            writer.writerow(reader[0])
            
            # Iterate through rows and update only the specific task
            for row in reader[1:]:
                if row[0] == task_number:
                    # Only update LastCompleted for the specific task
                    if repeating == 'Yes':
                        row[5] = datetime.now().strftime('%Y-%m-%d')
                    # If not repeating, this will effectively remove the task
                
                # Write the row back (either updated or unchanged)
                if repeating == 'Yes' or row[0] == task_number:
                    writer.writerow(row)
        
        # Reload tasks to reflect changes
        self.load_tasks()

def main():
    app = wx.App()
    frame = TodoTimerApp()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
