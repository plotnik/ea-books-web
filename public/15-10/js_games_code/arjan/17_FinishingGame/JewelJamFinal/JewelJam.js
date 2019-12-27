"use strict";

var ID = {};
var sprites = {};
var sounds = {};

Game.loadAssets = function () {
    var loadSprite = function (sprite) {
        return Game.loadSprite("../../assets/JewelJam/sprites/" + sprite);
    };

    var loadSound = function (sound, looping) {
        return new Sound("../../assets/JewelJam/sounds/" + sound, looping);
    };

    sprites.background = loadSprite("spr_background.jpg");
    sprites.frame_score = loadSprite("spr_frame_score.jpg");
    sprites.button_help = loadSprite("spr_button_help.jpg");
    sprites.frame_help = loadSprite("spr_frame_help.png");
    sprites.jewelcart = loadSprite("spr_jewelcart.png");
    sprites.jewels = loadSprite("spr_jewels@27.png");
    if (Touch.isTouchDevice) {
        sprites.gameover = loadSprite("spr_gameover_tap.png");
        sprites.title = loadSprite("spr_title_tap.jpg");
    } else {
        sprites.gameover = loadSprite("spr_gameover_click.png");
        sprites.title = loadSprite("spr_title_click.jpg");
    }
    sprites.frame_selector = loadSprite("spr_frame_selector.png");
    sprites.glitter = loadSprite("spr_glitter.png");
    sprites.double = loadSprite("spr_double.png");
    sprites.triple = loadSprite("spr_triple.png");

    sounds.music = loadSound("snd_music", true);
    sounds.combi = loadSound("snd_combi");
    sounds.double = loadSound("snd_double");
    sounds.triple = loadSound("snd_triple");
    sounds.gameover = loadSound("snd_gameover");
};

Game.initialize = function () {
    // play the music
    sounds.music.volume = 0.3;
    sounds.music.play();

    // define the layers
    ID.layer_background = 1;
    ID.layer_background_1 = 2;
    ID.layer_background_2 = 3;
    ID.layer_background_3 = 4;
    ID.layer_tiles = 10;
    ID.layer_objects = 20;
    ID.layer_objects_1 = 21;
    ID.layer_objects_2 = 22;
    ID.layer_overlays = 30;
    ID.layer_overlays_1 = 31;
    ID.layer_overlays_2 = 32;

    // define object IDs
    ID.title = 1;
    ID.help_frame = 2;
    ID.jewel_cart = 3;
    ID.grid = 4;
    ID.game_over = 5;
    ID.score = 6;
    ID.double_timer = 7;
    ID.triple_timer = 8;

    // create the game world
    Game.gameWorld = new JewelJamGameWorld();
};













