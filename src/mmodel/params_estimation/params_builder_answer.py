def get_params(params, muncps, popt, id=0):
    params_estimated = []

    for id, munc in enumerate(muncps):
        start = id*len(params)
        end = start+len(params)
        estimation = {}

        print(munc)
        print("params: ")
        for i, p in enumerate(popt[start:end]):
            print(f'{params[i%len(params)]}: {p}')
            estimation[params[i % len(params)]] = p
        params_estimated.append(estimation)
        print("")
    return params_estimated
