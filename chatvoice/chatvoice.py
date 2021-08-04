#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Ivan Vladimir Meza Ruiz 2018
# GPL 3.0

# imports
import click
from click_option_group import optgroup
import sys
import configparser
import os.path

# local imports
from .conversation import Conversation
#from audio import audio_close, audio_devices, list_voices
#import torch
#  class Classifier(torch.nn.Module):
                        #  def __init__(self, MODEL_NAME):
                        #      super(Classifier, self).__init__()
                        #      # Store the model we want to use
                        #      # We need to create the model and tokenizer
                        #      self.l1 =BertModel.from_pretrained(MODEL_NAME)
                        #      if MODEL_NAME=="skimai/electra-small-spanish":
                        #        self.pre_classifier = torch.nn.Linear(256, 256)
                        #        self.classifier = torch.nn.Linear(256, 2)
                        #      else:
                        #        self.pre_classifier = torch.nn.Linear(768, 768) # bert full
                        #        self.classifier = torch.nn.Linear(768, 2) # bert full
                        #      self.dropout = torch.nn.Dropout(0.3)

                        #  def forward(self, input_ids, attention_mask):
                        #      output_1 = self.l1(input_ids=input_ids, attention_mask=attention_mask)
                        #      hidden_state = output_1[0]
                        #      pooler = hidden_state[:, 0]
                        #      pooler = self.pre_classifier(pooler)
                        #      pooler = torch.nn.ReLU()(pooler)
                        #      pooler = self.dropout(pooler)
                        #      output = self.classifier(pooler)
                        #      return output

# Main service
CONFIG='DEFAULT'
config = configparser.ConfigParser()
@click.group()
@click.argument("conversation-file")
@click.option('--config-filename', type=click.Path(), default="config.ini")
@click.option("-v", "--verbose",
        is_flag=True,
        help="Verbose mode [%(default)s]")
@click.pass_context
def chatvoice(ctx,conversation_file=None,config_filename="config.ini",verbose=False):
    global CONFIG
    global config
    ctx.ensure_object(dict)
    if os.path.exists(config_filename):
        config.read(config_filename)
    if conversation_file:
        extra_settings=os.path.splitext(os.path.basename(conversation_file))[0]
        if extra_settings in config:
            CONFIG=extra_settings
    ctx.obj['config']=config
    ctx.obj['conversation_file']=conversation_file
    ctx.obj['config_section']=CONFIG
    ctx.obj['verbose']=verbose


@chatvoice.command()
@optgroup.group('Paths', help='Paths to auxiliary files')
@optgroup.option("--audios-dir",
        default=config.get(CONFIG,'audios_dir',fallback='audios'),
        type=click.Path(),
        help="Prefix directory for audios [%(default)s]")
@optgroup.option("--speech-recognition-dir",
        default=config.get(CONFIG,'speech_recognition_dir',fallback='speech_recognition'),
        type=click.Path(),
        help="Directory for audios for speech recognition [%(default)s]")
@optgroup.option("--tts-dir",
        default=config.get(CONFIG,'tts_dir',fallback='tts'),
        type=click.Path(),
        help="Directory for audios for tts [%(default)s]")
@optgroup.option("--is-filename",
        default=config.get(CONFIG,'is_filename',fallback='is.json'),
        type=click.Path(),
        help="File to save the Information State (remember) filename [%(default)s]")
@optgroup.option("--audio-tts-db",
        default=config.get(CONFIG,'audio_tts_db',fallback='audios_tts.tinydb'),
        type=click.Path(),
        help="File to store information about the audios generated by the tts [%(default)s]")
@optgroup.group('Conversation', help='Conversation files')
@optgroup.option("--generate-all-tts",
        default=config.get(CONFIG,'generate_all_tts',fallback=False),
        is_flag=True,
        help="During tts generate all audios, do not use the database [%(default)s]")
@optgroup.option("--remember-all",
        default=config.get(CONFIG,'remember_all',fallback=False),
        is_flag=True,
        help="Remember all slots from conversation [%(default)s]")
@optgroup.group('Speech', help='Options to control speech processing [%(default)s]')
@optgroup.option("--speech-recognition",
        default=config.getboolean(CONFIG,'speech_recognition',fallback=False),
        is_flag=True,
        help="Activate speech recognition [%(default)s]")
@optgroup.option("--tts",
        default=config.getboolean(CONFIG,'tts',fallback=None),
        type=click.Choice([None,'local', 'google'], case_sensitive=False),
        help="Select the tts to use [%(default)s]")
@optgroup.option("--local-tts-voice",
        default=config.get(CONFIG,'local_tts_voice',fallback='spanish-latin-am'),
        type=str,
        help="Use espeak local tts [%(default)s]")
@optgroup.option("--google-tts-language",
        default=config.get(CONFIG,'google_tts_langage',fallback='es-us'),
        type=str,
        help="Use espeak local tts [%(default)s]")
@optgroup.group('Audio', help='Options to control audio')
@optgroup.option("--samplerate",type=int,
        default=config.getint(CONFIG,'samplerate',fallback=48000),
        is_flag=True,
        help="Samplerate [%(default)s]")
@optgroup.option("--num-channels",type=int,
        default=config.getint(CONFIG,'num-channels',fallback=2),
        is_flag=True,
        help="Number of channels microphone [%(default)s]")
@optgroup.option("--device",
        default=config.getint(CONFIG,'device',fallback=None),
        is_flag=True,
        help="Device number to connect audio [%(default)s]")
@optgroup.option("--aggressiveness",
        default=config.getint(CONFIG,'aggressiveness',fallback=None),
        is_flag=True,
        help="VAD aggressiveness [%(default)s]")
@click.pass_context
def console(ctx,
        **args
        ):
    """Lauches a chatvoice for console
    """
    CONFIG=dict(args)
    CONFIG['main_path']=os.path.dirname(ctx.obj["conversation_file"])
    CONFIG['verbose']=ctx.obj["verbose"]

    # Main conversation
    conversation = Conversation(
            filename=ctx.obj["conversation_file"],
            **CONFIG)

    conversation.execute()

if __name__ == '__main__':
    chatvoice(obj={})