import depth_counter1

class TestMath:
    def test_depth(self, mocker):
        mocked_cwd = mocker.patch("os.getcwd")
        mocked_cwd.return_value = "/"
        assert depth_counter1.get_cwd_depth()==1
