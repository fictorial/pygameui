import random
import sys

sys.path.insert(0, '..')
import pygameui as ui


LIST_WIDTH = 180
MARGIN = 20
SMALL_MARGIN = 10


class KitchenSinkScene(ui.Scene):
    def __init__(self):
        ui.Scene.__init__(self)

        self.background_color = ui.theme.scene_background_color

        self.name_textfield = ui.TextField(
            frame=ui.Rect(MARGIN, MARGIN, 200,
            ui.theme.label_height), placeholder='Your name')
        self.name_textfield.centerx = self.frame.centerx
        self.add_child(self.name_textfield)

        gridview = ui.GridView(ui.Rect(0, 0, 500, 500))
        self.scroll_gridview = ui.ScrollView(ui.Rect(
            MARGIN, self.name_textfield.frame.bottom + MARGIN,
            200 - ui.theme.scrollbar_size, 250), gridview)
        self.add_child(self.scroll_gridview)

        items = ['Apples', 'Bananas', 'Grapes', 'Cheese', 'Goats', 'Beer']
        labels = [ui.Label(ui.Rect(
            0, 0, LIST_WIDTH, ui.theme.label_height), item)
            for item in items]
        for l in labels:
            l.halign = ui.LEFT
        list_view = ui.ListView(ui.Rect(0, 0, LIST_WIDTH, 400), labels)
        list_view.on_selected.connect(self.selected)
        list_view.on_deselected.connect(self.deselected)
        self.scroll_list = ui.ScrollView(ui.Rect(
            MARGIN, self.scroll_gridview.frame.bottom + MARGIN,
            LIST_WIDTH, 80), list_view)
        self.add_child(self.scroll_list)

        text_width = ui.theme.default_bold_font.size('Submit')[0]
        self.greet_button = ui.Button(ui.Rect(
            self.name_textfield.frame.right + SMALL_MARGIN,
            self.name_textfield.frame.top,
            text_width + ui.theme.padding * 2,
            ui.theme.button_height), 'Submit')
        self.greet_button.on_clicked.connect(self.greet)
        self.add_child(self.greet_button)

        self.image_view = ui.view_for_image_named('logo')
        self.image_view.frame.right = self.frame.right - MARGIN
        self.image_view.frame.top = MARGIN
        self.add_child(self.image_view)

        self.checkbox = ui.Checkbox(ui.Rect(
            self.scroll_gridview.frame.right + MARGIN,
            self.scroll_gridview.frame.top,
            200, ui.theme.label_height), 'I eat food')
        self.checkbox.toggle()
        self.add_child(self.checkbox)

        self.checkbox1 = ui.Checkbox(ui.Rect(
            self.checkbox.frame.left,
            self.checkbox.frame.bottom + SMALL_MARGIN,
            200, ui.theme.label_height), 'I drink water')
        self.checkbox1.toggle()
        self.add_child(self.checkbox1)

        self.checkbox2 = ui.Checkbox(ui.Rect(
            self.checkbox.frame.left,
            self.checkbox1.frame.bottom + SMALL_MARGIN,
            200, ui.theme.label_height), 'I exercise regularly')
        self.add_child(self.checkbox2)

        info_image = ui.get_image('info')
        self.info_button = ui.ImageButton(ui.Rect(
            self.checkbox2.frame.left,
            self.checkbox2.frame.bottom + MARGIN,
            0, 0), info_image)
        self.info_button.on_clicked.connect(self.show_alert)
        self.add_child(self.info_button)

        notify_image = ui.get_image('star')
        self.notify_button = ui.ImageButton(ui.Rect(
            self.info_button.frame.right + SMALL_MARGIN,
            self.info_button.frame.top,
            0, 0), notify_image)
        self.notify_button.on_clicked.connect(self.show_notification)
        self.add_child(self.notify_button)

        self.task_button = ui.Button(ui.Rect(
            self.info_button.frame.left,
            self.info_button.frame.bottom + MARGIN,
            150, ui.theme.button_height), 'Consume!')
        self.task_button.on_clicked.connect(self.run_fake_task)
        self.add_child(self.task_button)

        self.running_task = False
        self.progress_view = ui.ProgressView(ui.Rect(
            self.task_button.frame.right + MARGIN,
            self.task_button.frame.centery - ui.theme.scrollbar_size // 2,
            180, ui.theme.scrollbar_size))
        self.add_child(self.progress_view)
        self.progress_view.hidden = True

        labels2 = [ui.Label(
            ui.Rect(0, 0, LIST_WIDTH, ui.theme.label_height),
            'Item %d' % (i + 1)) for i in range(10)]
        for l in labels2:
            l.halign = ui.LEFT
        self.select_view = ui.SelectView(ui.Rect(
            self.task_button.frame.left,
            self.task_button.frame.bottom + MARGIN,
            LIST_WIDTH, ui.theme.label_height), labels2)
        self.select_view.on_selection_changed.connect(self.selection_changed)
        self.add_child(self.select_view)

        self.hslider = ui.SliderView(ui.Rect(
            self.select_view.frame.left,
            self.select_view.frame.bottom + MARGIN,
            100, ui.theme.scrollbar_size), ui.HORIZONTAL, 0, 100)
        self.hslider.on_value_changed.connect(self.value_changed)
        self.add_child(self.hslider)

        self.vslider = ui.SliderView(ui.Rect(
            self.hslider.frame.right + SMALL_MARGIN,
            self.hslider.frame.centery,
            ui.theme.scrollbar_size, 100), ui.VERTICAL, 0, 100)
        self.vslider.on_value_changed.connect(self.value_changed)
        self.add_child(self.vslider)

        self.slider_value = ui.Label(ui.Rect(
            self.hslider.frame.centerx - 25,
            self.hslider.frame.bottom + MARGIN,
            50, ui.theme.label_height), '')
        self.slider_value.border_width = 1
        self.slider_value.border_color = ui.theme.border_color
        self.slider_value.background_color = ui.theme.view_background_color
        self.add_child(self.slider_value)

        self.spinner = ui.SpinnerView(ui.Rect(
            self.frame.right - MARGIN - ui.SpinnerView.size,
            self.frame.bottom - MARGIN - ui.SpinnerView.size,
            0, 0))
        self.add_child(self.spinner)

    def selected(self, list_view, item, index):
        item.background_color = ui.theme.selected_background_color
        item.text_color = ui.theme.selected_text_color

    def deselected(self, list_view, item, index):
        item.background_color = ui.theme.clear_color
        item.text_color = ui.theme.text_color

    def selection_changed(self, selection_view, item, index):
        print 'new selection: %s' % str(item)

    def value_changed(self, slider_view, value):
        self.slider_value.text = '%d' % value

    def greet(self, btn, mbtn):
        name = self.name_textfield.text.strip()
        if len(name) == 0:
            name = 'uh, you?'
        ui.scene.current.add_child(ui.AlertView(
            'Greetings!', 'Hello, %s' % name, ui.OK))

    def show_alert(self, btn, mbtn):
        msgs = [
            'This is an alert',
            'This is an alert with\na line break in it',
            'This is a rather long alert that should ' +
            'automatically word wrap to multiple lines',
            'This is an very long alert that should ' +
            'automatically word wrap to multiple lines...' +
            'is this not the best thing EVAR? wow, mindblowing...'
        ]
        msg = random.choice(msgs)
        ui.scene.current.add_child(ui.AlertView('Info', msg, ui.OK))

    def show_notification(self, btn, mbtn):
        msgs = [
           'Achievement Unlocked! Notification!',
           'This is a notification\nwith a linebreak in it',
           'This notification is rather long and should ' +
           'automatically word wrap to multiple lines'
        ]
        msg = random.choice(msgs)
        ui.scene.current.add_child(ui.NotificationView(msg))

    def run_fake_task(self, btn, mbtn):
        if not self.running_task:
            self.task_button.set_enabled(False)
            self.progress_view.hidden = False
        self.progress_view.progress = 0
        self.running_task = True

    def update(self, dt):
        ui.Scene.update(self, dt)
        if self.running_task:
            progress = min(1.0, self.progress_view.progress + 0.01)
            self.progress_view.progress = progress
            self.running_task = (self.progress_view.progress < 1.0)
            self.task_button.set_enabled(not self.running_task)
            if self.task_button.interactive:
                msg = "I'M FINISHED!"
                alert_view = ui.AlertView('Milkshake', msg, ui.OK)
                ui.scene.current.add_child(alert_view)
                self.progress_view.progress = 0
                self.progress_view.hidden = True


if __name__ == '__main__':
    ui.init('pygameui - Kitchen Sink')
    ui.scene.push(KitchenSinkScene())
    ui.run()
