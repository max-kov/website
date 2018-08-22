import depth_counter2

class TestMath:
    def test_mock_in_os(self, mocker):
        mocked_cwd = mocker.patch("os.getcwd")
        mocked_cwd.return_value = "/"
        assert depth_counter2.get_cwd_depth()==1

    def test_mock_in_depth_counter(self, mocker):
        mocked_cwd = mocker.patch("depth_counter2.getcwd")
        mocked_cwd.return_value = "/"
        assert depth_counter2.get_cwd_depth()==1
