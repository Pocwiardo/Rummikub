from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import random
import numpy as np
import sys
import graphics_rc
from timer import Timer
from tile import Tile
from player import Player
from desk import ForegroundItem
from logger import Logger
from options import OptionsDialog
from database import DatabaseSQL, DatabaseXML
from board import Board
import sqlite3

class Replay(QGraphicsScene):
    def __init__(self, view, players, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, 1800, 1000)

        try:
            background_image = QImage(":/backgr/wood3.jpg")
            background_brush = QBrush(
                background_image.scaled(self.width(), self.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            self.setBackgroundBrush(background_brush)
        except:
            self.setBackgroundBrush(QBrush(QColor(238, 238, 238)))
        self.tiles = []

        self.current_player_index = 0
        self.tile_width = Tile.width
        self.tile_height = Tile.height
        self.foreground_item = ForegroundItem(self.tile_width * 20, self.tile_height * 2)
        self.foreground_item.setPos(self.sceneRect().width() / 2 - self.tile_width * 20 / 2, int(round(
            (self.sceneRect().height() - self.tile_height * 2) / self.tile_height)) * self.tile_height)
        self.addItem(self.foreground_item)

        self.players = players
        # umieszczenie nazw graczy
        self.player_name_items = []
        y = 800
        for i, player in enumerate(self.players):
            name_item = QGraphicsTextItem(player.name)
            name_item.setFont(QFont("Arial", 16, QFont.Bold))
            name_item.setDefaultTextColor(QColor(235, 235, 235))
            if i == self.current_player_index:
                name_item.setDefaultTextColor(QColor(255, 100, 100))
            self.addItem(name_item)
            name_item.setPos(50, y)
            self.player_name_items.append(name_item)
            y += 30



        self.move_number = 0
        conn = sqlite3.connect('rummikub_game.db')
        self.cursor = conn.cursor()

        self.cursor.execute('SELECT COUNT(DISTINCT move_index) FROM board_tiles')
        self.max_moves = self.cursor.fetchone()[0]

        self.move_number_widget = QLabel(f"ruch: {self.move_number}/{self.max_moves}")
        self.move_number_widget.setFont(QFont("Arial", 16))
        self.move_number_widget.setAlignment(Qt.AlignRight)
        self.addWidget(self.move_number_widget)
        self.move_number_widget.setGeometry(1500, 20, 250, 30)

        # create the buttons and connect them to the corresponding slots
        self.increment_button = QPushButton("+")
        self.increment_button.clicked.connect(self.increment_move_number)
        self.decrement_button = QPushButton("-")
        self.decrement_button.clicked.connect(self.decrement_move_number)

        # add the buttons to the scene
        self.addWidget(self.increment_button)
        self.addWidget(self.decrement_button)

        # position the buttons
        self.increment_button.setGeometry(1600, 800, 50, 50)
        self.decrement_button.setGeometry(1700, 800, 50, 50)

        # call retrieve_tiles to draw the initial state
        self.retrieve_tiles()

    def increment_move_number(self):
        self.move_number += 1
        if self.move_number > self.max_moves:
            self.move_number = self.max_moves
        self.update_move_number()
        self.clear()
        self.retrieve_tiles()

    def decrement_move_number(self):
        self.move_number -= 1
        if self.move_number < 0:
            self.move_number = 0
        self.update_move_number()
        self.clear()
        self.retrieve_tiles()

    def retrieve_tiles(self):
        # retrieve the tiles for the current move from the database
        self.cursor.execute('SELECT * FROM board_tiles WHERE move_index = ?', (self.move_number,))
        tiles = self.cursor.fetchall()

        # iterate over the tiles and place them on the board
        for tile_data in tiles:
            number, color, row, col = tile_data[1:]
            if number == 0:
                tile = Tile(color, number, is_joker=True)
            else:
                tile = Tile(color, number)
            #print(tile)
            tile.setPosFromIndices(row, col)
            self.addItem(tile)

    def clear(self):
        # remove only Tile objects from the scene
        for item in self.items():
            if isinstance(item, Tile):
                self.removeItem(item)

    def update_move_number(self):
        self.move_number_widget.setText(f"ruch: {self.move_number}/{self.max_moves}")