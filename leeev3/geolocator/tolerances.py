class Tolerances(object):
    # TODO: Add units to all of these, and make sure we are using meters everywhere
    ParallelLineSlopeDelta = 0.01
    SlopeCalculationMinimumDeltaX = 0.01
    SamplingEpsilon = 0.005  # m
    ColorTolerance = 3  # distance out of 256 for two color values to be equal (as in 0, 0, 1 equals 0, 0, 3)
    NumberGridSamples = 100  # how many grid points to break the x or y dimension in to for searching for a color
    NumberAngularSamples = 40  # how many angular samples to take when searching around a known location
    TwoPointsEqualDistance = 0.005  # half of a cm
