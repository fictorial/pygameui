from gui import *


class TestScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        self.btn1 = Button('Alert')
        self.btn1.frame = rect(0, 0, 0, 30)
        self.btn1.size_to_fit()
        self.btn1.frame.left = 10
        self.btn1.frame.bottom = self.frame.bottom - 10
        self.btn1.on_clicked.add(lambda btn: self.show_alert('Hello, world!'))
        self.add_child(self.btn1)

        self.sl = Slider()
        self.sl.frame = rect(10, 150, 100, 20)
        self.sl.value = 0.5  # [0,1]
        self.add_child(self.sl)

        self.pr = Progress()
        self.pr.frame = rect(10, 180, 100, 20)
        self.pr.value = 0.25  # [0,1]
        self.add_child(self.pr)

        self.btn2 = Button('Start')
        self.btn2.frame = rect(0, self.pr.frame.bottom + 10, 0, 30)
        self.btn2.size_to_fit()
        self.btn2.frame.centerx = self.pr.frame.centerx
        self.btn2.on_clicked.add(self.run_progress)
        self.add_child(self.btn2)
        self.running_task = False

        self.lst = List(['Item %s' % str(i) for i in range(10)])
        self.lst.frame = rect(self.frame.w // 2, 10, 150, 170)
        self.lst.frame.w = self.lst.container.frame.w
        self.lst.selected_index = 1
        self.add_child(self.lst)

        self.cb1 = Checkbox('I eat food')
        self.cb1.frame = rect(self.lst.frame.left, 
                              self.lst.frame.bottom + 50, 0, 0)
        self.cb1.size_to_fit()
        self.cb1.checked = True
        self.add_child(self.cb1)

        self.cb2 = Checkbox('I drink water')
        self.cb2.frame = rect(self.cb1.frame.left,
                              self.cb1.frame.bottom + 10, 0, 0)
        self.cb2.size_to_fit()
        self.cb2.checked = True
        self.add_child(self.cb2)

        self.cb3 = Checkbox('I exercise regularly')
        self.cb3.frame = rect(self.cb1.frame.left,
                              self.cb2.frame.bottom + 10, 0, 0)
        self.cb3.size_to_fit()
        self.add_child(self.cb3)

        self.tf1 = TextField()
        self.tf1.frame = rect(10, 10, 150, 30)
        self.tf1.on_return.add(lambda tf, text: self.show_alert('You entered: %s' % text))
        self.add_child(self.tf1)

        self.tf2 = TextField()
        self.tf2.frame = rect(10, 50, 150, 30)
        self.add_child(self.tf2)

        self.logo = Image('logo.png')
        self.logo.size_to_fit()
        self.logo.frame.right = self.frame.right - 10
        self.logo.frame.top = 10
        self.add_child(self.logo)

        self.spinner = Spinner()
        self.spinner.frame.right = self.frame.right - Spinner.size - 10
        self.spinner.frame.bottom = self.frame.bottom - Spinner.size - 10
        self.add_child(self.spinner)

    def run_progress(self, button):
        self.pr.value = 0.0
        self.running_task = True

    def update(self, dt):
        Scene.update(self, dt)
        if self.running_task:
            self.pr.value += 0.1 * dt
            if self.pr.value == 1.0:
                self.running_task = False
                self.show_alert('Simulated task finished!')


if __name__ == '__main__':
    run(TestScene)

