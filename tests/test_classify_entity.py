from classify_entity import ClassifyEntity


class TestClassifyEntity:
    """ """

    def test_alex_classify(self, entities_json_path, flags_json_path, docs_dir):
        """ """
        classify = ClassifyEntity(entities_json_path, flags_json_path, docs_dir)
        assert classify is not None
