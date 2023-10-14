from classify_entity import ClassifyEntity


class TestClassifyEntity:
    """ """

    def test_alex_classify(self, entities_json_path, flags_json_path):
        """ """
        classify = ClassifyEntity(entities_json_path, flags_json_path)
        assert classify is not None
