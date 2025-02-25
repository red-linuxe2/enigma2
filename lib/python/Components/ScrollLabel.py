from __future__ import absolute_import
from __future__ import division
import skin
from Components.GUIComponent import GUIComponent
from enigma import eLabel, eWidget, eSlider, fontRenderClass, ePoint, eSize


class ScrollLabel(GUIComponent):
	def __init__(self, text="", showscrollbar=True):
		GUIComponent.__init__(self)
		self.message = text
		self.showscrollbar = showscrollbar
		self.instance = None
		self.long_text = None
		self.right_text = None
		self.scrollbar = None
		self.TotalTextHeight = 0
		self.curPos = 0
		self.pageHeight = 0
		self.column = 0
		self.split = False
		self.splitchar = "|"
		self.lineheight = None
		self.scrollbarmode = "showOnDemand"

	def applySkin(self, desktop, parent):
		scrollbarWidth = 10
		itemHeight = 30
		scrollbarBorderWidth = 1
		ret = False
		if self.skinAttributes:
			widget_attribs = []
			scrollbar_attribs = []
			remove_attribs = []
			for (attrib, value) in self.skinAttributes:
				if "itemHeight" in attrib:
					itemHeight = int(value)
					remove_attribs.append((attrib, value))
				if "scrollbarMode" in attrib:
					self.scrollbarmode = value
					remove_attribs.append((attrib, value))
				if "borderColor" in attrib or "borderWidth" in attrib:
					scrollbar_attribs.append((attrib, value))
				if "transparent" in attrib or "backgroundColor" in attrib:
					widget_attribs.append((attrib, value))
				if "scrollbarSliderForegroundColor" in attrib:
					scrollbar_attribs.append((attrib, value))
					remove_attribs.append((attrib, value))
				if "scrollbarSliderBorderColor" in attrib:
					scrollbar_attribs.append((attrib, value))
					remove_attribs.append((attrib, value))
				if "scrollbarSliderPicture" in attrib:
					scrollbar_attribs.append((attrib, value))
					remove_attribs.append((attrib, value))
				if "scrollbarBackgroundPicture" in attrib:
					scrollbar_attribs.append((attrib, value))
					remove_attribs.append((attrib, value))
				if "scrollbarWidth" in attrib:
					scrollbarWidth = int(value)
					remove_attribs.append((attrib, value))
				if "scrollbarSliderBorderWidth" in attrib:
					scrollbarBorderWidth = int(value)
					remove_attribs.append((attrib, value))
				if "split" in attrib:
					self.split = int(value)
					if self.split:
						self.right_text = eLabel(self.instance)
					self.skinAttributes.remove((attrib, value))
				if "colposition" in attrib:
					self.column = int(value)
				if "dividechar" in attrib:
					self.splitchar = value
			for (attrib, value) in remove_attribs:
				self.skinAttributes.remove((attrib, value))
			if self.split:
				skin.applyAllAttributes(self.long_text, desktop, self.skinAttributes + [("halign", "left")], parent.scale)
				skin.applyAllAttributes(self.right_text, desktop, self.skinAttributes + [("transparent", "1"), ("halign", "left" if self.column else "right")], parent.scale)
			else:
				skin.applyAllAttributes(self.long_text, desktop, self.skinAttributes, parent.scale)
			skin.applyAllAttributes(self.instance, desktop, widget_attribs, parent.scale)
			skin.applyAllAttributes(self.scrollbar, desktop, scrollbar_attribs + widget_attribs, parent.scale)
			ret = True
		self.pageWidth = self.long_text.size().width()
		self.lineheight = fontRenderClass.getInstance().getLineHeight(self.long_text.getFont()) or itemHeight # assume a random lineheight if nothing is visible
		lines = int(self.long_text.size().height() / self.lineheight)
		self.pageHeight = int(lines * self.lineheight)
		self.instance.move(self.long_text.position())
		self.instance.resize(eSize(self.pageWidth, self.pageHeight + int(self.lineheight / 6)))
		self.scrollbar.move(ePoint(self.pageWidth - scrollbarWidth, 0))
		self.scrollbar.resize(eSize(scrollbarWidth, self.pageHeight + int(self.lineheight / 6)))
		self.scrollbar.setOrientation(eSlider.orVertical)
		self.scrollbar.setRange(0, 100)
		self.scrollbar.setBorderWidth(scrollbarBorderWidth)
		self.setText(self.message)
		return ret

	def setPos(self, pos):
		self.curPos = max(0, min(pos, self.TotalTextHeight - self.pageHeight))
		self.long_text.move(ePoint(0, -self.curPos))
		self.split and self.right_text.move(ePoint(self.column, -self.curPos))

	def setText(self, text, showBottom=False):
		self.message = text
		text = text.rstrip()
		if self.pageHeight:
			if self.split:
				left = []
				right = []
				for line in text.split("\n"):
					line = line.split(self.splitchar, 1)
					left.append(line[0])
					right.append("" if len(line) < 2 else line[1].lstrip())
				self.long_text.setText("\n".join(left))
				self.right_text.setText("\n".join(right))
			else:
				self.long_text.setText(text)
			self.TotalTextHeight = self.long_text.calculateSize().height()
			self.long_text.resize(eSize(self.pageWidth - 30, self.TotalTextHeight))
			self.split and self.right_text.resize(eSize(self.pageWidth - self.column - 30, self.TotalTextHeight))
			if showBottom:
				self.lastPage()
			else:
				self.setPos(0)
			if (self. scrollbarmode == "showAlways") or ((self.scrollbarmode == "showOnDemand") and self.showscrollbar and self.TotalTextHeight > self.pageHeight):
				self.scrollbar.show()
				self.updateScrollbar()
			else:
				self.scrollbar.hide()

	def appendText(self, text, showBottom=True):
		self.setText(self.message + text, showBottom)

	def pageUp(self):
		if self.TotalTextHeight > self.pageHeight:
			self.setPos(self.curPos - self.pageHeight)
			self.updateScrollbar()

	def pageDown(self):
		if self.TotalTextHeight > self.pageHeight:
			self.setPos(self.curPos + self.pageHeight)
			self.updateScrollbar()

	def lastPage(self):
		self.setPos(self.TotalTextHeight - self.pageHeight)

	def isAtLastPage(self):
		return self.TotalTextHeight <= self.pageHeight or self.curPos == self.TotalTextHeight - self.pageHeight

	def updateScrollbar(self):
		vis = max(100 * self.pageHeight // self.TotalTextHeight, 3)
		start = (100 - vis) * self.curPos // (self.TotalTextHeight - self.pageHeight)
		self.scrollbar.setStartEnd(start, start + vis)

	def GUIcreate(self, parent):
		self.instance = eWidget(parent)
		self.scrollbar = eSlider(self.instance)
		self.long_text = eLabel(self.instance)

	def GUIdelete(self):
		self.long_text = None
		self.scrollbar = None
		self.instance = None
		self.right_text = None

	def getText(self):
		return self.message
