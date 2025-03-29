import asyncio
import logging
import sys
from abc import ABC, abstractmethod
from typing import List

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

dp = Dispatcher()

class ReplyCommand(ABC):
    commands: List[str]
    buttons: List[List[KeyboardButton]]
    keybord: ReplyKeyboardMarkup

    def __init_subclass__(cls, **kwargs):

        if not hasattr(cls, 'commands'):
            raise TypeError(f"class {cls.__name__} must define an attribute 'commands'")
        if not hasattr(cls, 'buttons'):
            raise TypeError(f"class {cls.__name__} must define an attribute 'buttons'")
        if not hasattr(cls, 'keybord'):
            raise TypeError(f"class {cls.__name__} must define an attribute 'keybord'")
        return super().__init_subclass__(**kwargs)

    @staticmethod 
    @abstractmethod
    async def execute(): ...


class ReplyRegisterCommand:
    def __init__(
            self, command: str|List[str] = None, handler = dp.message,):
        self.command = command
        self.handler = handler
    
    def __call__(self, cls: ReplyCommand):
        if not self.command:
            self.command = list(cls.commands)

        filter = lambda message: message.text in self.command
        self.handler(filter)(cls.execute)
        return cls


class CategorySelectionMenu:
    commands = []


class SearchOptionMenu(ReplyCommand):
    commands = ['Категории', 'Жанры', 'Поиск по названию']
    buttons = [[KeyboardButton(text=com) for com in commands]]
    keybord = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True)

    @staticmethod
    async def execute(message: Message):
        match message.text:
            case 'Категории':
                pass
            case 'Жанры':
                pass
            case 'Поиск по названию':
                pass
            case _:
                raise


@ReplyRegisterCommand()
class MainMenu(ReplyCommand):
    commands = ['Найти книгу','Добавить книгу']
    buttons = [[KeyboardButton(text=com) for com in commands]]
    keybord = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True)
    
    @staticmethod
    async def execute(message: Message):
        match message.text:
            case 'Найти книгу':
                await message.answer('Выберите критерий поиска', reply_markup=SearchOptionMenu.keybord)
            case 'Добавить книгу':
                pass
            case _:
                raise


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(
        f'Hello, {html.bold(message.from_user.full_name)}',
        reply_markup=MainMenu.keybord)