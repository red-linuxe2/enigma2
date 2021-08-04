# Embedded file name: /usr/lib/enigma2/python/Components/Frame.py
from HTMLComponent import HTMLComponent
from GUIComponent import GUIComponent
from VariableText import VariableText
from skin import parseSize
from enigma import eFrame, eSize

class Frame(VariableText, HTMLComponent, GUIComponent):

    def __init__(self, text = '', onClick = []):
        GUIComponent.__init__(self)
        VariableText.__init__(self)
        self.setText(text)
        self.onClick = onClick
        # self.onAnimationEnd = []
        self.skinSize = eSize(0, 0)

    def checkSingleAttribute(self, skinAttributes):
        attribs = []
        for attrib, value in skinAttributes:
            if attrib == 'size':
                self.skinSize = parseSize(value, ((1, 1), (1, 1)))
                attribs.append((attrib, value))
            # elif attrib == 'css':
            #     from skin import cascadingStyleSheets
            #     styles = value.split(',')
            #     for style in styles:
            #         for _attrib in cascadingStyleSheets[style].keys():
            #             _value = cascadingStyleSheets[style][_attrib]
            #             attribs = attribs + self.checkSingleAttribute([(_attrib, _value)])

            else:
                attribs.append((attrib, value))

        return attribs

    def applySkin(self, desktop, screen):
        if self.skinAttributes is not None:
            self.skinAttributes = self.checkSingleAttribute(self.skinAttributes)
        return GUIComponent.applySkin(self, desktop, screen)

    def push(self):
        for x in self.onClick:
            x()

        return 0

    # def animationEnd(self):
    #     for f in self.onAnimationEnd:
    #         f()

    #     return 0

    def disable(self):
        pass

    def enable(self):
        pass

    def produceHTML(self):
        return '<input type="submit" text="' + self.getText() + '">\n'

    GUI_WIDGET = eFrame

    def postWidgetCreate(self, instance):
        instance.setText(self.text or '')
        instance.selected.get().append(self.push)
        # instance.animationEnd.get().append(self.animationEnd)

    def preWidgetRemove(self, instance):
        instance.selected.get().remove(self.push)
        # instance.animationEnd.get().remove(self.animationEnd)

    def getSkinSize(self):
        return self.skinSize