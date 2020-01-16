import os
from fixtures.testdata import barb_fixtures
from barbutils import generate_barb, load_barb
import numpy as np

script_path = os.path.dirname(os.path.realpath(__file__))

for key in barb_fixtures.keys():
    generated = generate_barb(barb_fixtures[key][0], barb_fixtures[key][1])

    with open(os.path.join(script_path, "fixtures", key), "rb") as f:
        fixture = f.read()

    sample_rate, data = load_barb(fixture)
    assert sample_rate == barb_fixtures[key][1]
    np.testing.assert_allclose(data, barb_fixtures[key][0], rtol=1e-3)

    loaded_sample_rate, loaded_data = load_barb(generated)
    assert loaded_sample_rate == barb_fixtures[key][1]
    np.testing.assert_allclose(loaded_data, barb_fixtures[key][0], rtol=1e-3)

