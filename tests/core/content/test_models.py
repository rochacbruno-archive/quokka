import pytest
import mock
import click
import functools
from quokka.core.content.utils import url_for_content
from quokka.core.content.formats import get_format
from quokka.core.content.paginator import Paginator
from flask import url_for
from flask import current_app as app
from quokka.utils.text import (
    slugify, slugify_category, make_social_link,
    make_social_name, make_external_url
)
from quokka.utils.dateformat import pretty_date
from quokka.utils.custom_vars import custom_var_dict
from quokka.core.content.models import (
    Orderable, Series, Category, Fixed, Url, Author,
    Tag, Content, Article, Page, Block, BlockItem,
    make_model, make_paginator
)


################################################################################
#pytest - fixtures                                                             #
################################################################################
DEFAULT_DATE_FORMAT = '%a %d %B %Y'

class MockExtendsOrderableTestClass(Orderable):
    def debug_is_content(self):
        return self.is_content

series = Series("mock-name")
category = Category("mock-category")
fixed = Fixed(name="mock-name")
url = Url(name="mock-name")
author = Author(authors="mock-authors")
tag = Tag(name="mock-name")


#######################################################
#pytest - Quokka - tests/core/content/test_models.py  #
#######################################################
def test_Orderable():
    meotc = MockExtendsOrderableTestClass()
    assert meotc.is_content == False

def test_SeriesClass_all_property():
    assert series.all == []

def test_SeriesClass_all_next():
    assert series.all_next == []

def test_SeriesClass_all_prrevious():
    assert series.all_previous == []

def test_SeriesClass_index():
    assert series.index == 1

def test_SeriesClass_is_content():
    assert series.is_content == False

def test_SeriesClass_name():
    assert series.name == 'mock-name'

def test_SeriesClass_next():
    assert series.next == []

def test_SeriesClass_previous():
    assert series.previous == []

def test_SeriesClass_slug():
    assert series.slug == 'mock-name'
 
def test_Series_class_property_external_url_atribute_error():

    with pytest.raises(AttributeError) as err:
        try:
            series.external_url(url="mock-url")
            assert "object has no attribute url" in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        
        except RuntimeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise

 
def test_Category_class_property_external_url_atribute_error():

    with pytest.raises(RuntimeError) as err:
        try:
            category.external_url
            assert "Working outside of request context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        
        except AttributeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise


def test_Category_class_property_category():
    assert category.category == 'mock-category'

def test_Category_class_property_is_content():
    assert category.is_content == False

def test_Category_class_property_name():
    assert category.name == 'Mock Category'

def test_Category_class_property_slug():
    assert category.slug == 'mock-category'

def test_Category_class_property_url():
    assert category.url == 'mock-category'

def test_Fixed_class_property_is_content():
    assert fixed.is_content == False

def test_Fixed_class_property_name():
    assert fixed.name == 'mock-name'

def test_Fixed_class_property_slug():
    assert fixed.slug == 'mock-name'

def test_Fixed_class_property_url():    
    assert fixed.url == 'mock-name'

def test_Fixed_class_property_external_url_atribute_error():

    with pytest.raises(RuntimeError) as err:
        try:
            fixed.external_url
            assert "Working outside of request context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        
        except AttributeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise


def test_Url_class_property_is_content():
    assert url.is_content == False

def test_Url_class_property_name():
    assert url.name == 'mock-name'

def test_Url_class_property_slug():
    assert url.slug == 'mock-name'

def test_Url_class_property_url():    
    assert url.url == 'mock-name'

def test_Url_class_property_external_url_atribute_error():

    with pytest.raises(RuntimeError) as err:
        try:
            url.external_url
            assert "Working outside of request context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        
        except AttributeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise


def test_class_Authors_property_authors():
    assert author.authors == 'mock-authors'

def test_class_Authors_property_is_content():
    assert author.is_content == False

def test_class_Authors_property_name():
    assert author.name == 'Mock Authors'

def test_class_Authors_property_slug():
    assert author.slug == 'mock-authors'

def test_class_Authors_property_social():
    assert author.social == {}

def test_class_Authors_property_url():
    assert author.url == 'author/mock-authors'

def test_class_Tag_property_is_content():
    assert tag.is_content == False

def test_class_Tag_property_name():
    assert tag.name == 'mock-name'

def test_class_Tag_property_slug():
    assert tag.slug == 'mock-name'

def test_class_Tag_property_url():
    assert tag.url == 'tag/mock-name/index.html'


def test_Content_class_property_external_url_atribute_error():

    with pytest.raises(RuntimeError) as err:
        try:
            content = Content(data="2018-11-01")
            assert "working outside of request context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.eexist:
                raise

        except AttributeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise


def test_Article_class_property_external_url_atribute_error():

    with pytest.raises(RuntimeError) as err:
        try:
            article = Article(data="2018-11-01")
            assert "working outside of request context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.eexist:
                raise

        except AttributeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise


def test_Page_class_property_external_url_atribute_error():

    with pytest.raises(RuntimeError) as err:
        try:
            page = Page(data="2018-11-01")
            assert "working outside of request context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.eexist:
                raise

        except AttributeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise


def test_Block_class_property_external_url_atribute_error():

    with pytest.raises(RuntimeError) as err:
        try:
            block = Block(data="2018-11-01")
            assert "working outside of request context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.eexist:
                raise

        except AttributeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise

def test_BlockItem_class_property_external_url_atribute_error():

    with pytest.raises(RuntimeError) as err:
        try:
            block = BlockItem(data="2018-11-01")
            assert "working outside of request context." in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.eexist:
                raise

        except AttributeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise



