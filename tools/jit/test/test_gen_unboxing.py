import tempfile
import unittest
from unittest.mock import patch, NonCallableMock

import tools.jit.gen_unboxing as gen_unboxing


@patch("tools.jit.gen_unboxing.get_custom_build_selector")
@patch("tools.jit.gen_unboxing.parse_native_yaml")
@patch("tools.jit.gen_unboxing.make_file_manager")
@patch("tools.jit.gen_unboxing.gen_unboxing")
class TestGenUnboxing(unittest.TestCase):
    def test_get_custom_build_selector_with_allowlist(
        self,
        mock_gen_unboxing: NonCallableMock,
        mock_make_file_manager: NonCallableMock,
        mock_parse_native_yaml: NonCallableMock,
        mock_get_custom_build_selector: NonCallableMock,
    ) -> None:
        args = ["--op_registration_allowlist=op1", "--op_selection_yaml_path=path2"]
        gen_unboxing.main(args)
        mock_get_custom_build_selector.assert_called_once_with(["op1"], "path2")

    def test_get_custom_build_selector_with_allowlist_yaml(
        self,
        mock_gen_unboxing: NonCallableMock,
        mock_make_file_manager: NonCallableMock,
        mock_parse_native_yaml: NonCallableMock,
        mock_get_custom_build_selector: NonCallableMock,
    ) -> None:
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.write(b"- aten::add.Tensor")
        temp_file.seek(0)
        args = [
            f"--TEST_ONLY_op_registration_allowlist_yaml_path={temp_file.name}",
            "--op_selection_yaml_path=path2",
        ]
        gen_unboxing.main(args)
        mock_get_custom_build_selector.assert_called_once_with(
            ["aten::add.Tensor"], "path2"
        )
        temp_file.close()

    def test_get_custom_build_selector_with_both_allowlist_and_yaml(
        self,
        mock_gen_unboxing: NonCallableMock,
        mock_make_file_manager: NonCallableMock,
        mock_parse_native_yaml: NonCallableMock,
        mock_get_custom_build_selector: NonCallableMock,
    ) -> None:
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.write(b"- aten::add.Tensor")
        temp_file.seek(0)
        args = [
            "--op_registration_allowlist=op1",
            "--TEST_ONLY_op_registration_allowlist_yaml_path={temp_file.name}",
            "--op_selection_yaml_path=path2",
        ]
        gen_unboxing.main(args)
        mock_get_custom_build_selector.assert_called_once_with(["op1"], "path2")
        temp_file.close()


if __name__ == "__main__":
    unittest.main()
