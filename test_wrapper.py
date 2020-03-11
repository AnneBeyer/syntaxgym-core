from agg_surprisals import aggregate_surprisals
from suite import Sentence
import nose
import json

def test_eos_sos():
    regions = [
        {"region_number": 1, "content": "This"},
        {"region_number": 2, "content": "is"},
        {"region_number": 3, "content": "a"},
        {"region_number": 4, "content": "test."}
    ]
    with open("dummy_specs/eos_sos.json", "r") as f:
        spec = json.load(f)
    tokens = "<s> This is a test . </s>".split()
    unks = [0, 0, 0, 0, 0, 0, 0]
    sentence = Sentence(spec, tokens, unks, regions=regions)
    print(sentence.region2tokens)
    assert sentence.region2tokens == {
        1: ["<s>", "This"],
        2: ["is"],
        3: ["a"],
        4 : ["test", ".", "</s>"]
    }

def test_unk():
    regions = [
        {"region_number": 1, "content": "This"},
        {"region_number": 2, "content": "is WEIRDADVERB"},
        {"region_number": 3, "content": "a"},
        {"region_number": 4, "content": "WEIRDNOUN."}
    ]
    with open("dummy_specs/basic.json", "r") as f:
        spec = json.load(f)
    tokens = "This is <unk> a <unk> .".split()
    unks = [0, 0, 1, 0, 1, 0]
    sentence = Sentence(spec, tokens, unks, regions=regions)
    assert sentence.oovs == {
        0: [],
        1: ["WEIRDADVERB"],
        2: [],
        3 : ["WEIRDNOUN"]
    }

def test_consecutive_unk():
    regions = [
        {"region_number": 1, "content": "This"},
        {"region_number": 2, "content": "is"},
        {"region_number": 3, "content": "a"},
        {"region_number": 4, "content": "WEIRDADVERB test WEIRDADJECTIVE WEIRDNOUN."}
    ]
    with open("dummy_specs/basic.json", "r") as f:
        spec = json.load(f)
    tokens = "This is a <unk> test <unk> <unk> <unk>".split()
    unks = [0, 0, 0, 1, 0, 1, 1, 1]
    sentence = Sentence(spec, tokens, unks, regions=regions)
    assert sentence.oovs == {
        3 : ["WEIRDADVERB", "WEIRDADJECTIVE", "WEIRDNOUN", "."]
    }

def test_empty_region():
    regions = [
        {"region_number": 1, "content": ""},
        {"region_number": 2, "content": "This"},
        {"region_number": 3, "content": "is"},
        {"region_number": 4, "content": ""},
        {"region_number": 5, "content": "a test."},
        {"region_number": 6, "content": ""}
    ]
    with open("dummy_specs/basic.json", "r") as f:
        spec = json.load(f)
    tokens = "This is a test .".split()
    unks = [0, 0, 0, 0, 0]
    sentence = Sentence(spec, tokens, unks, regions=regions)
    assert sentence.region2tokens == {
        1: [],
        2: ["This"],
        3: ["is"], 
        4: [],
        5: ["a", "test", "."],
        6: []
    }

def test_punct_region():
    regions = [
        {"region_number": 1, "content": "This"},
        {"region_number": 2, "content": "is"},
        {"region_number": 3, "content": ","},
        {"region_number": 4, "content": "a"},
        {"region_number": 5, "content": "test"},
        {"region_number": 6, "content": "."}
    ]
    with open("dummy_specs/basic.json", "r") as f:
        spec = json.load(f)
    tokens = "This is , a test .".split()
    unks = [0, 0, 0, 0, 0, 0]
    sentence = Sentence(spec, tokens, unks, regions=regions)
    assert sentence.region2tokens == {
        1: ["This"],
        2: ["is"],
        3: [","],
        4: ["a"],
        5 : ["test"],
        6: ["."]
    }

def test_uncased():
    """
    Test uncased vocabulary.
    """
    regions = [
        {"region_number": 1, "content": "This"},
        {"region_number": 2, "content": "is"},
        {"region_number": 3, "content": "a"},
        {"region_number": 4, "content": "test."}
    ]
    with open("dummy_specs/basic_uncased.json", "r") as f:
        spec = json.load(f)
    tokens = "this is a test .".split()
    unks = [0, 0, 0, 0, 0]
    sentence = Sentence(spec, tokens, unks, regions=regions)
    print(sentence.region2tokens)
    assert sentence.region2tokens == {
        1: ["this"],
        2: ["is"],
        3: ["a"],
        4 : ["test", "."]
    }

def test_remove_punct():
    regions = [
        {"region_number": 1, "content": "This!"},
        {"region_number": 2, "content": "?is"},
        {"region_number": 3, "content": ","},
        {"region_number": 4, "content": "a ---"},
        {"region_number": 5, "content": "test"},
        {"region_number": 6, "content": "."}
    ]
    with open("dummy_specs/basic_nopunct.json", "r") as f:
        spec = json.load(f)
    tokens = "This is a test".split()
    unks = [0, 0, 0, 0]
    sentence = Sentence(spec, tokens, unks, regions=regions)
    assert sentence.region2tokens == {
        1: ["This"],
        2: ["is"],
        3: [],
        4: ["a"],
        5 : ["test"],
        6: []
    }

# def test_special_types():
#     # TODO: if at region boundary, which region do we associate them with?
#     pass

# def test_bpe():
#     pass