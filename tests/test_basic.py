# -*- coding: utf-8 -*-

import logging

import click
from click.testing import CliRunner

import click_log

import pytest


test_logger = logging.getLogger(__name__)


@pytest.fixture
def runner():
    return CliRunner()


def test_basic(runner):
    @click.command()
    @click_log.init()
    def cli():
        test_logger.info('hey')
        test_logger.error('damn')

    result = runner.invoke(cli, catch_exceptions=False)
    assert not result.exception
    assert result.output == 'hey\nerror: damn\n'


def test_multilines(runner):
    @click.command()
    @click_log.init()
    def cli():
        test_logger.warning("""
            Lorem ipsum dolor sit amet,
            consectetur adipiscing elit,
            sed do eiusmod tempor incididunt""")

    result = runner.invoke(cli, catch_exceptions=False)
    assert not result.exception
    assert result.output == (
        'warning: \n'
        'warning:             Lorem ipsum dolor sit amet,\n'
        'warning:             consectetur adipiscing elit,\n'
        'warning:             sed do eiusmod tempor incididunt\n')


def test_unicode(runner):
    @click.command()
    @click_log.init()
    def cli():
        test_logger.error(u"""
            ❤️ 💔 💌 💕 💞 💓 💗 💖 💘
            💝 💟 💜 💛 💚 💙""")

    result = runner.invoke(cli, catch_exceptions=False)
    assert not result.exception
    assert result.output == (
        'error: \n'
        u'error:             ❤️ 💔 💌 💕 💞 💓 💗 💖 💘\n'
        u'error:             💝 💟 💜 💛 💚 💙\n')


def test_weird_types_log(runner):
    @click.command()
    @click_log.init()
    def cli():
        test_logger.error(42)
        test_logger.error('42')
        test_logger.error(b'42')
        test_logger.error(u'42')

    result = runner.invoke(cli, catch_exceptions=False)
    assert not result.exception
    assert result.output == 'error: 42\n' * 4
