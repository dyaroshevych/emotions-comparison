# Book vs Film Emotions Comparison

This package allows you to dive deeper into the art of H.G. Wells by showing you how huge amounts of emotions in films do not make them better than corresponding books. It allows the user to either compare a single book and film or get an analysis based on author's all works.

## Installation

### Option 1: Quick Way (with clean data)

1. Install the package.

```sh
pip install emotions_comparison
```

### Option 2: Long Way (with raw data)

1. Install the package.

```sh
pip install emotions_comparison
```

2. Download databases with raw data and put them in 'data' folder in the same directory as your script:
   <https://bit.ly/3mzEal7>

3. Import datasets module from the package into your Python script and generate formatted datasets.

```python3
from emotions_comparison import datasets

datasets.generate_datasets()
```

## Usage example

Import the main module from the package into your Python script and run the main function.

```python3
from emotions_comparison import main

main.main()
```

You will be asked to make a choice:

![preview-1](https://drive.google.com/file/d/1Ri-KKczTBblq7mcskkcC9ajZdrbM_WHl/view?usp=sharing)

If your choice was to compare a single book and film, you will be asked to choose which ones and then given the data.
![preview-2](https://drive.google.com/file/d/17Vdrq3Pihcv0393VptmsGiSd4vR3otRq/view?usp=sharing)
![preview-3](https://drive.google.com/file/d/1fxDJZhbwBAEQyhFURVUI95N4XAKuj2Ue/view?usp=sharing)

## Meta

Your Name – [@dyaroshevych](https://twitter.com/dyaroshevych) – dyaroshevych@gmail.com

Distributed under the MIT license. See `LICENSE` for more information.

[https://github.com/dyaroshevych/emotions-comparison](https://github.com/dyaroshevych/)

## Contributing

1. Fork it (<https://github.com/dyaroshevych/emotions-comparion/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
