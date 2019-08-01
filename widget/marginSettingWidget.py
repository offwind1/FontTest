from PyQt5.QtWidgets import *


class BaseWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initialize()
        self.setLayouts()
        self.setConfigs()
        self.setStyles()

    def initialize(self):
        pass

    def setLayouts(self):
        pass

    def setConfigs(self):
        pass

    def setStyles(self):
        pass


class LabelSpinbox(QFrame):
    def __init__(self, tag):
        super().__init__()
        self.tag = tag

        self.initialize()
        self.setLayouts()
        self.setConfigs()
        self.setStyles()

    def initialize(self):
        self.label = QLabel(self.tag)
        self.spinbox = QSpinBox()

    def setLayouts(self):
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.spinbox)
        layout.addStretch(1)

        self.setLayout(layout)

    def setConfigs(self):
        pass

    def setStyles(self):
        self.spinbox.setMinimum(0)
        self.spinbox.setMaximum(9999)

        self.label.setContentsMargins(0, 0, 0, 0)
        self.spinbox.setContentsMargins(0, 0, 0, 0)

        self.setContentsMargins(0, 0, 0, 0)

    def value(self):
        return self.spinbox.value()


class MarginSettingWidget(BaseWidget):

    def initialize(self):
        self.top_widget = LabelSpinbox("上")
        self.left_widget = LabelSpinbox("左")
        self.down_widget = LabelSpinbox("下")
        self.right_widget = LabelSpinbox("右")

    def setLayouts(self):



        pass
        line1 = QHBoxLayout()
        line1.addWidget(self.top_widget)
        line1.addWidget(self.down_widget)

        line2 = QHBoxLayout()
        line2.addWidget(self.left_widget)
        line2.addWidget(self.right_widget)

        layout = QVBoxLayout()
        layout.addLayout(line1)
        layout.addLayout(line2)

        self.setLayout(layout)

    def setConfigs(self):
        pass

    def setStyles(self):
        pass
