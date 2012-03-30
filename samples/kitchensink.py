import pygame

import random
import sys

sys.path.insert(0, '..')
from pygameui import *
import pygameui


LIST_WIDTH = 180
MARGIN = 20
SMALL_MARGIN = 10


class KitchenSinkScene(scene.Scene):
    def __init__(self):
        scene.Scene.__init__(self)

        self.background_color = theme.scene_background_color

        self.name_textfield = textfield.TextField(
            frame=pygame.Rect(MARGIN, MARGIN, 200,
            theme.label_height), placeholder='Your name')
        self.name_textfield.centerx = window.rect.centerx
        self.add_child(self.name_textfield)

        gridview = grid.GridView(pygame.Rect(0, 0, 500, 500))
        self.scroll_gridview = scroll.ScrollView(
            pygame.Rect(MARGIN, self.name_textfield.frame.bottom + MARGIN,
            200 - theme.scrollbar_size, 250), gridview)
        self.add_child(self.scroll_gridview)

        items = ['Apples', 'Bananas', 'Grapes', 'Cheese', 'Goats', 'Beer']
        labels = [label.Label(
            pygame.Rect(0, 0, LIST_WIDTH, theme.label_height),
            item) for item in items]
        for l in labels:
            l.halign = label.LEFT
        list_view = listview.ListView(pygame.Rect(0, 0, LIST_WIDTH, 400),
            labels)
        list_view.on_selected.connect(self.selected)
        list_view.on_deselected.connect(self.deselected)
        self.scroll_list = scroll.ScrollView(pygame.Rect(MARGIN,
            self.scroll_gridview.frame.bottom + MARGIN, LIST_WIDTH, 80),
            list_view)
        self.add_child(self.scroll_list)

        self.greet_button = button.Button(pygame.Rect(
            self.name_textfield.frame.right + SMALL_MARGIN,
            self.name_textfield.frame.top,
            asset.default_bold_font.size('Submit')[0] + theme.padding * 2,
            theme.button_height), 'Submit')
        self.greet_button.on_clicked.connect(self.greet)
        self.add_child(self.greet_button)

        self.image_view = \
            imageview.ImageView.view_for_image_named('logo')
        self.image_view.frame.right = self.frame.right - MARGIN
        self.image_view.frame.top = MARGIN
        self.add_child(self.image_view)

        self.checkbox = checkbox.Checkbox(pygame.Rect(
            self.scroll_gridview.frame.right + MARGIN,
            self.scroll_gridview.frame.top,
            200, theme.label_height), 'I eat food')
        self.checkbox.toggle()
        self.add_child(self.checkbox)

        self.checkbox1 = checkbox.Checkbox(pygame.Rect(
            self.checkbox.frame.left,
            self.checkbox.frame.bottom + SMALL_MARGIN,
            200, theme.label_height), 'I drink water')
        self.checkbox1.toggle()
        self.add_child(self.checkbox1)

        self.checkbox2 = checkbox.Checkbox(pygame.Rect(
            self.checkbox.frame.left,
            self.checkbox1.frame.bottom + SMALL_MARGIN,
            200, theme.label_height), 'I exercise regularly')
        self.add_child(self.checkbox2)

        info_image = asset.get_image('info')
        self.info_button = imagebutton.ImageButton(pygame.Rect(
            self.checkbox2.frame.left,
            self.checkbox2.frame.bottom + MARGIN,
            0, 0), info_image)
        self.info_button.on_clicked.connect(self.show_alert)
        self.add_child(self.info_button)

        notify_image = asset.get_image('star')
        self.notify_button = imagebutton.ImageButton(pygame.Rect(
            self.info_button.frame.right + SMALL_MARGIN,
            self.info_button.frame.top,
            0, 0), notify_image)
        self.notify_button.on_clicked.connect(self.show_notification)
        self.add_child(self.notify_button)

        self.task_button = button.Button(pygame.Rect(
            self.info_button.frame.left,
            self.info_button.frame.bottom + MARGIN,
            150, theme.button_height), 'Consume!')
        self.task_button.on_clicked.connect(self.run_fake_task)
        self.add_child(self.task_button)

        self.running_task = False
        self.progress_view = progress.ProgressView(pygame.Rect(
            self.task_button.frame.right + MARGIN,
            self.task_button.frame.centery - theme.scrollbar_size // 2,
            180, theme.scrollbar_size))
        self.add_child(self.progress_view)
        self.progress_view.hidden = True

        labels2 = [label.Label(
            pygame.Rect(0, 0, LIST_WIDTH, theme.label_height),
            'Item %d' % (i + 1)) for i in range(10)]
        for l in labels2:
            l.halign = label.LEFT
        self.select_view = select.SelectView(pygame.Rect(
            self.task_button.frame.left,
            self.task_button.frame.bottom + MARGIN,
            LIST_WIDTH, theme.label_height), labels2)
        self.select_view.on_selection_changed.connect(self.selection_changed)
        self.add_child(self.select_view)

        self.hslider = slider.SliderView(pygame.Rect(
            self.select_view.frame.left,
            self.select_view.frame.bottom + MARGIN,
            100, theme.scrollbar_size), slider.HORIZONTAL, 0, 100)
        self.hslider.on_value_changed.connect(self.value_changed)
        self.add_child(self.hslider)

        self.vslider = slider.SliderView(pygame.Rect(
            self.hslider.frame.right + SMALL_MARGIN,
            self.hslider.frame.centery,
            theme.scrollbar_size, 100), slider.VERTICAL, 0, 100)
        self.vslider.on_value_changed.connect(self.value_changed)
        self.add_child(self.vslider)

        self.slider_value = label.Label(pygame.Rect(
            self.hslider.frame.centerx - 25,
            self.hslider.frame.bottom + MARGIN,
            50, theme.label_height), '')
        self.slider_value.border_width = 1
        self.slider_value.border_color = theme.border_color
        self.slider_value.background_color = theme.view_background_color
        self.add_child(self.slider_value)

        self.spinner = spinner.SpinnerView(pygame.Rect(
            window.rect.right - MARGIN - spinner.SpinnerView.size,
            window.rect.bottom - MARGIN - spinner.SpinnerView.size,
            0, 0))
        self.add_child(self.spinner)

    def selected(self, list_view, item, index):
        item.background_color = theme.selected_background_color
        item.text_color = theme.selected_text_color

    def deselected(self, list_view, item, index):
        item.background_color = theme.clear_color
        item.text_color = theme.text_color

    def selection_changed(self, selection_view, item, index):
        print 'new selection: %s' % str(item)

    def value_changed(self, slider_view, value):
        self.slider_value.text = '%d' % value

    def greet(self, btn, mbtn):
        name = self.name_textfield.text.strip()
        if len(name) == 0:
            name = 'uh, you?'
        scene.current.add_child(alert.AlertView('Greetings!',
            'Hello, %s' % name, alert.OK))

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
        scene.current.add_child(alert.AlertView('Info', msg, alert.OK))

    def show_notification(self, btn, mbtn):
        msgs = [
           'Achievement Unlocked! Notification!',
           'This is a notification\nwith a linebreak in it',
           'This notification is rather long and should ' +
           'automatically word wrap to multiple lines'
        ]
        msg = random.choice(msgs)
        scene.current.add_child(notification.NotificationView(msg))

    def run_fake_task(self, btn, mbtn):
        if not self.running_task:
            self.task_button.set_enabled(False)
            self.progress_view.hidden = False
        self.progress_view.set_progress(0.0)
        self.running_task = True

    def update(self, dt):
        scene.Scene.update(self, dt)
        if self.running_task:
            progress = min(1.0, self.progress_view.progress() + 0.01)
            self.progress_view.set_progress(progress)
            self.running_task = (self.progress_view.progress() < 1.0)
            self.task_button.set_enabled(not self.running_task)
            if self.task_button.interactive:
                msg = "I'M FINISHED!"
                alert_view = alert.AlertView('Milkshake', msg, alert.OK)
                scene.current.add_child(alert_view)
                self.progress_view.set_progress(0)
                self.progress_view.hidden = True


if __name__ == '__main__':
    pygameui.init('pygameui - Kitchen Sink')
    scene.pushscene(KitchenSinkScene())
    pygameui.run()
