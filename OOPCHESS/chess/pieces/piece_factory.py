from chess.constants import PieceType
from chess.moves.moves import ChessPosition

from chess.king.king import King
from chess.queen.queen import Queen
from chess.knight.knight import Knight
from chess.rook.rook import Rook
from chess.bishop.bishop import Bishop
from chess.pawn.pawn import Pawn

class PieceFactory:
    @staticmethod
    def create(piece_type: str, position: ChessPosition, color):
        if piece_type == PieceType.KING:
            return King(position, color)
        
        if piece_type == PieceType.QUEEN:
            return Queen(position, color)
        
        if piece_type == PieceType.KNIGHT:
            return Knight(position, color)
        
        if piece_type == PieceType.ROOK:
            return Rook(position, color)
        
        if piece_type == PieceType.BISHOP:
            return Bishop(position, color)
        
        if piece_type == PieceType.PAWN:
            return Pawn(position, color)