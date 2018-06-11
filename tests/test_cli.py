from quokka import create_app
import pytest, os, errno, pathlib, os.path
import pytest_mock
import pytest_django
from quokka.cli import copyfolder, with_app


directory_pwd = os.getcwd()+"/tests/"
directory_test = "copy-directory-test/"
file_test = "cli-test-file"

def test_copy_folder_error_first_param():
    
    with pytest.raises(FileNotFoundError) as error:
        
        try:
            copyfolder("", directory_pwd+directory_test+file_test)        
            assert "No such file or directory" in str(error.value)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        except RuntimeError:
            raise

        except FileExistsError:
            raise


def test_copy_folder_error_second_param():
    
    with pytest.raises(FileNotFoundError) as error:
        
        try:
            copyfolder(directory_pwd+file_test, "")        
            assert "No such file or directory" in str(error.value)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        except RuntimeError:
            raise

        except FileExistsError:
            raise


def test_copy_folder_file_exists():
    
    try:
        copyfolder(directory_pwd+file_test, directory_pwd+directory_test+file_test)        
        assert os.path.isfile(directory_pwd+directory_test+file_test) is True

    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        
    except RuntimeError:
         raise


#def test_with_app():
    #@with_app
    
    #def mock_fun():
        #return True
    
    #assert mock_fun.decorated is True

def test_check():
    pass

def test_init():
    pass

def test_adduser():
    pass

def execute():
    pass

def mais():
    pass
