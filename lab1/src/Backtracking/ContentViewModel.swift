import Foundation
import SwiftUI

extension ContentView {
    class ViewModel: ObservableObject {
        @Published var gridSize: Int = 7
        @Published var incorrectGrid: Bool = false
        @Published var squares = [Square]()
        @Published var squareSize = CGFloat(0)

        func placeSqures(_ tableSize: CGFloat) {
            squares = []
            var bestCount: Int32 = 0
            let bestSolution = getBestSolution(&bestCount, Int32(gridSize))
            
            for i in 0..<Int(bestCount) {
                let x = bestSolution![i]![0]
                let y = bestSolution![i]![1]
                let size = bestSolution![i]![2]
                
                let square = Square(x: CGFloat(x), y: CGFloat(y), size: CGFloat(size), color: .random())
                squares.append(square)
            }
            squareSize = tableSize / CGFloat(gridSize)
        }
    }
}

struct Square {
    var x: CGFloat
    var y: CGFloat
    var size: CGFloat
    var color: Color
}
