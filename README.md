# prototype_asr_assistant
Just a prototype of an ASR assistant using Flashlight and Wav2Letter (see <https://github.com/flashlight/flashlight>), shared at the request of (see <https://github.com/flashlight/flashlight/discussions/601>).

I am unsure of what one will have to do to actually get the code working on their machine. At the least one will have to download an acoustic model and language model and put them in the inference_tutorial folder (this should work <wget https://dl.fbaipublicfiles.com/wav2letter/rasr/tutorial/am_transformer_ctc_stride3_letters_300Mparams.bin>, <wget https://dl.fbaipublicfiles.com/wav2letter/rasr/tutorial/lm_common_crawl_small_4gram_prun0-6-15_200kvocab.bin>). And one will have to create a build folder in which to build InferenceCTC.cpp.
