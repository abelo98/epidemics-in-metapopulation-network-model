def get_params(params, muncps, popt):
    params_estimated = []

    for munc in muncps:
        estimation = {}

        print(munc)
        print("params: ")
        for i, p in enumerate(popt):
            print(f'{params[i%len(params)]}: {p}')
            estimation[params[i % len(params)]] = p
        params_estimated.append(estimation)
        print("")
    return params_estimated
